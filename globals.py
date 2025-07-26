import pygame as pg

bg_color = (8, 6, 10)

class InputBox():
    font = None
    BOX_COLOR = (80, 80, 80)
    BOX_COLOR_LIGHT = (110, 110, 110)

    def __init__(self, position, tooltip, tag='', width=300, height=80):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(center=position)
        self.font = pg.font.Font(None, 25)
        self.text = ''
        self.tag = tag
        self.tooltip = tooltip

        self._redraw()

    def _redraw(self):
        self.image.fill(pg.Color(self.BOX_COLOR))
        self.image.fill(pg.Color(self.BOX_COLOR_LIGHT), (0, 0, self.rect.width, 30))

        tooltip_surf = self.font.render(self.tooltip, True, 'white')
        self.image.blit(tooltip_surf, (10, 7))

        text_surf = self.font.render(self.text, True, 'white')
        text_rect = pg.Rect(0, 0, self.rect.width - 16, 28)
        text_rect.midleft = (14, self.rect.height - 20)
        self.image.blit(text_surf, text_rect)

        input_field_rect = pg.Rect(0, 0, self.rect.width - 16, 28)
        input_field_rect.midleft = (8, self.rect.height - 25)
        pg.draw.rect(self.image, self.BOX_COLOR_LIGHT, input_field_rect, width=2)

    def on_text_input(self, event):
        self.text += event.text
        self._redraw()

    def on_key_down(self, event):
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            self._redraw()