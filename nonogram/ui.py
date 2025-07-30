import pygame as pg

def get_ui_font():
    return pg.font.Font('segoeui.ttf', 18)

class EventManager:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, func):
        if event_type in self.listeners:
            self.listeners[event_type].append(func)
        else:
            self.listeners[event_type] = [func]

    def remove_listener(self, func):
        for event_type in self.listeners.keys():
            if func in self.listeners[event_type]:
                self.listeners[event_type].remove(func)

    def manage_events(self):
        for event in pg.event.get():
            for listener in self.listeners.get(event.type, []):
                listener(event)

class InputBox(pg.sprite.Sprite):
    BOX_COLOR = (80, 80, 80)
    BOX_COLOR_LIGHT = (110, 110, 110)

    def __init__(self, position, tooltip, on_enter, event_manager, tag='', width=300, height=80):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(center=position)
        self.font = get_ui_font()
        self.text = ''
        self.tag = tag
        self.tooltip = tooltip
        self.on_enter = on_enter

        self.event_manager = event_manager
        self.event_manager.add_listener(pg.TEXTINPUT, self.on_text_input)
        self.event_manager.add_listener(pg.KEYDOWN, self.on_key_down)

        self._redraw()

    def _redraw(self):
        self.image.fill(pg.Color(self.BOX_COLOR))
        self.image.fill(pg.Color(self.BOX_COLOR_LIGHT), (0, 0, self.rect.width, 30))

        tooltip_surf = self.font.render(self.tooltip, True, 'white')
        self.image.blit(tooltip_surf, tooltip_surf.get_rect(left=10, centery=14))

        text_surf = self.font.render(self.text, True, 'white')
        # text_rect = pg.Rect(0, 0, self.rect.width - 16, 28)
        # text_rect.midleft = (14, self.rect.height - 20)
        self.image.blit(text_surf, text_surf.get_rect(left=14, centery=self.rect.height - 26))

        input_field_rect = pg.Rect(0, 0, self.rect.width - 16, 28)
        input_field_rect.midleft = (8, self.rect.height - 25)
        pg.draw.rect(self.image, self.BOX_COLOR_LIGHT, input_field_rect, width=2)

    def kill(self):
        super().kill()
        self.event_manager.remove_listener(self.on_key_down)
        self.event_manager.remove_listener(self.on_text_input)

    def on_text_input(self, event):
        self.text += event.text
        self._redraw()

    def on_key_down(self, event):
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            self._redraw()
        elif event.key == pg.K_RETURN:
            self.on_enter()
            self.kill()

class Button(pg.sprite.Sprite):
    BG_COLOR = (90, 90, 90)
    BORDER_COLOR = (20, 20, 20)

    def __init__(self, position, on_click, text, event_manager, tag='', width=None, height=40):
        super().__init__()
        self.font = get_ui_font()
        self.text = text
        self.tag = tag
        self.on_click = on_click
        self.event_manager = event_manager

        if width is not None:
            self.image = pg.Surface((width, height))
            self.image.fill(pg.Color(self.BG_COLOR))
        else:
            text_surf = self.font.render(self.text, True, 'white')
            self.image = pg.Surface((text_surf.width + 30, height))
            self.image.fill(pg.Color(self.BG_COLOR))
            self.image.blit(text_surf, text_surf.get_rect(center=self.image.get_rect().center))

        self.rect = self.image.get_rect(center=position)
        pg.draw.rect(self.image, self.BORDER_COLOR, self.image.get_rect(topleft=(0, 0)), width=2)

        self.event_manager.add_listener(pg.MOUSEBUTTONDOWN, self.on_mousebutton_down)

    def kill(self):
        super().kill()
        self.event_manager.remove_listener(self.on_mousebutton_down)

    def on_mousebutton_down(self, event):
        if event.button == 1 and self.rect.collidepoint(pg.mouse.get_pos()):
            self.on_click()