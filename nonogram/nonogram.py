import json
import time
import pygame as pg
from itertools import groupby, product
from ui import EventManager, Button, InputBox, get_ui_font
import random


class Grid:
    def __init__(self, matrix, rect=pg.Rect(0, 0, 0, 0)):
        self.matrix = matrix
        self.row_guides = self._get_row_guides()
        self.col_guides = self._get_col_guides()
        self.rect = rect

    # Returns a list of lists of numbers representing the consecutive black boxes in each row
    def _get_row_guides(self):
        guides = []

        for i in range(len(self.matrix)):
            nums = [len(list(group)) for key, group in groupby(self.get_row(i)) if key == 1]

            if not nums:
                guides.append([0])
            else:
                guides.append(nums)

        return guides

    # Returns a list of lists of numbers representing the consecutive black boxes in each column
    def _get_col_guides(self):
        guides = []

        for i in range(len(self.matrix)):
            nums = [len(list(group)) for key, group in groupby(self.get_col(i)) if key == 1]

            if not nums:
                guides.append([0])
            else:
                guides.append(nums)

        return guides

    # Returns the i-th column
    def get_col(self, i):
        return list(map(lambda row: row[i], self.matrix))

    # Returns the i-th row
    def get_row(self, i):
        return self.matrix[i]

    # Get the state of a box
    def get_box(self, row, col):
        return self.matrix[row][col]

    # Set the state of a box
    def set_box(self, row, col, state):
        self.matrix[row][col] = state
        self.row_guides = self._get_row_guides()
        self.col_guides = self._get_col_guides()


def draw_grid():
    # Draw grid boxes
    for i in range(grid_size):
        for j in range(grid_size):
            box_rect = (grid.rect.x + j * box_length, grid.rect.y + i * box_length, box_length + 1, box_length + 1)

            if grid.get_box(i, j) == 0:
                pg.draw.rect(screen, GRID_BG_COL, box_rect)
            elif grid.get_box(i, j) == 1:
                pg.draw.rect(screen, GRID_BORDER_COL, box_rect)
            elif grid.get_box(i, j) == 2:
                pg.draw.rect(screen, GRID_BG_COL, box_rect)
                screen.blit(cross_image, box_rect)

    # Draw grid lines
    for i in range(grid_size - 1):
        pass
        # Vertical line
        pg.draw.line(screen, LINE_COL,
                     (grid.rect.x + (i + 1) * box_length, grid.rect.y),
                     (grid.rect.x + (i + 1) * box_length, grid.rect.y + grid_size * box_length - 1))
        # Horizontal line
        pg.draw.line(screen, LINE_COL,
                     (grid.rect.x, grid.rect.y + (i + 1) * box_length),
                     (grid.rect.x + grid_size * box_length - 1, grid.rect.y + (i + 1) * box_length))

    for i in range(4, grid_size - 1, 5):
        # Vertical thick line
        pg.draw.line(screen, THICK_LINE_COL,
                     (grid.rect.x + (i + 1) * box_length, grid.rect.y),
                     (grid.rect.x + (i + 1) * box_length, grid.rect.y + grid_size * box_length - 1), 3)
        # Horizontal thick line
        pg.draw.line(screen, THICK_LINE_COL,
                     (grid.rect.x, grid.rect.y + (i + 1) * box_length),
                     (grid.rect.x + grid_size * box_length - 1, grid.rect.y + (i + 1) * box_length), 3)

    # Draw grid border
    pg.draw.rect(screen, GRID_BORDER_COL,
                 (grid.rect.x, grid.rect.y, box_length * grid_size, box_length * grid_size), 3)

    # Draw guides
    font_size = int(box_length * 22 // 48)
    guides_font = pg.font.Font('segoeui.ttf', font_size)
    spacing_hor = font_size * 0.8
    spacing_vert = font_size * 1.5

    for i in range(grid_size):
        nums = solution.row_guides[i]
        # If this row matches the solution guides, color the guides gray
        text_color = pg.Color('dark gray') if nums == grid.row_guides[i] else pg.Color('black')

        prev_left = grid.rect.left - 15 + spacing_hor
        for j in range(len(nums)):
            text = str(nums[-1 - j])
            text_surf = guides_font.render(text, True, text_color)
            text_rect = text_surf.get_rect(right=prev_left - spacing_hor,
                                           centery=grid.rect.top + box_length / 2 + i * box_length)
            screen.blit(text_surf, text_rect)
            prev_left = text_surf.get_rect(right=prev_left - spacing_hor).left

    for i in range(grid_size):
        nums = solution.col_guides[i]
        # If this column matches the solution guides, color the guides gray
        text_color = pg.Color('dark gray') if nums == grid.col_guides[i] else pg.Color('black')

        for j in range(len(nums)):
            text = str(nums[-1 - j])
            text_surf = guides_font.render(text, True, text_color)
            text_rect = text_surf.get_rect(bottom=grid.rect.top - 10 - j * spacing_vert,
                                           centerx=grid.rect.left + box_length / 2 + i * box_length)
            screen.blit(text_surf, text_rect)


def is_grid_solved():
    for i in range(grid_size):
        if not grid.row_guides[i] == solution.row_guides[i] or not grid.col_guides[i] == solution.col_guides[i]:
            return False

    return True


def on_quit(e):
    global running
    running = False


def on_mouse_down(e):
    global mb_pressed
    mb_pressed = e.button


def on_mouse_up(e):
    global mb_pressed, first_changed_state
    mb_pressed = 0
    first_changed_state = None


def on_key_down(e):
    if e.key == pg.K_ESCAPE:
        kill_sprites_with_tag('inputbox')


# Zooming
def on_mousewheel(e):
    global zoom, margin_topleft, box_length, grid, cross_image

    zoom_speed = 60
    margin_topleft = min(300 + grid_size * 0.1, margin_topleft - zoom_speed * e.y)
    box_length = (screen.width - MARGIN_BOTTOMRIGHT - margin_topleft) / grid_size

    mouse_x, mouse_y = pg.mouse.get_pos()
    prev_width = grid.rect.width
    prev_height = grid.rect.height
    grid.rect.width = box_length * grid_size
    grid.rect.height = box_length * grid_size
    grid.rect.x = grid.rect.x * grid.rect.width / prev_width - mouse_x * (grid.rect.width / prev_width - 1)
    grid.rect.y = grid.rect.y * grid.rect.height / prev_height - mouse_y * (grid.rect.height / prev_height - 1)

    cross_image = pg.transform.scale(orig_cross_image, (box_length, box_length))


# Panning
def on_mouse_motion(e):
    global margin_topleft

    if e.buttons[1]:
        delta_x, delta_y = e.rel
        grid.rect.x = max(-grid.rect.width + 10, min(screen.width - 10, grid.rect.x + delta_x))
        grid.rect.y = max(-grid.rect.height + 40, min(screen.height - 10, grid.rect.y + delta_y))


def on_mouse_pressed():
    mousex, mousey = pg.mouse.get_pos()
    col_clicked = (mousex - grid.rect.x) / box_length
    row_clicked = (mousey - grid.rect.y) / box_length

    toggle_map = {
        (1, 0): 1,
        (1, 1): 0,
        (3, 0): 2,
        (3, 2): 0,
    }

    if 0 < col_clicked < grid_size and 0 < row_clicked < grid_size:  # if mouse on grid
        row = int(row_clicked)
        col = int(col_clicked)
        box_state = grid.get_box(row, col)

        global first_changed_state
        if first_changed_state is None:
            first_changed_state = box_state

        # Only change state if this box has the same state as the box changed first with this mouse press
        if (mb_pressed, box_state) in toggle_map and box_state == first_changed_state:
            grid.set_box(row, col, toggle_map[(mb_pressed, box_state)])


def load_grid(name):
    global grid, solution, grid_size, box_length, margin_topleft, won, grid_name, start_time, cross_image

    with open(f'grids/{name}.json') as file:
        solution = Grid(json.load(file))

    grid_size = len(solution.matrix)
    margin_topleft = 200 + grid_size * 0.1
    box_length = (screen.width - MARGIN_BOTTOMRIGHT - margin_topleft) / grid_size
    grid = Grid([[0] * grid_size for _ in range(grid_size)],
                pg.Rect(margin_topleft, margin_topleft, box_length * grid_size, box_length * grid_size))
    won = False
    grid_name = name
    cross_image = pg.transform.scale(orig_cross_image, (box_length, box_length))
    start_time = time.time()


def on_load_button_pressed():
    kill_sprites_with_tag('inputbox')
    load_input_box = InputBox(screen.get_rect().center,
                              'Name of the grid to load:',
                              lambda: load_grid(load_input_box.text),
                              event_manager,
                              'inputbox')
    sprites.add(load_input_box)


def on_random_button_pressed():
    kill_sprites_with_tag('inputbox')
    random_input_box = InputBox(screen.get_rect().center,
                                'Size of the grid:',
                                lambda: create_random_grid(int(random_input_box.text)),
                                event_manager,
                                'inputbox')
    sprites.add(random_input_box)


def on_solve_button_pressed():
    for i in range(grid_size):
        for j in range(grid_size):
            grid.set_box(i, j, solution.get_box(i, j))


def create_random_grid(size):
    global grid, solution, grid_size, box_length, margin_topleft, won, grid_name, start_time, cross_image

    grid_size = size
    margin_topleft = 200 + grid_size * 0.1
    box_length = (screen.width - MARGIN_BOTTOMRIGHT - margin_topleft) / grid_size
    grid = Grid([[0] * grid_size for _ in range(grid_size)],
                pg.Rect(margin_topleft, margin_topleft, box_length * grid_size, box_length * grid_size))
    solution = Grid([[0] * grid_size for _ in range(grid_size)],
                    pg.Rect(margin_topleft, margin_topleft, box_length * grid_size, box_length * grid_size))
    won = False
    grid_name = ''
    cross_image = pg.transform.scale(orig_cross_image, (box_length, box_length))

    density = 0.7
    random_boxes = random.sample(list(product(range(size), repeat=2)), int((grid_size ** 2) * density))
    for box in random_boxes:
        solution.set_box(box[0], box[1], 1)

    start_time = time.time()


def kill_sprites_with_tag(tag):
    for sprite in sprites:
        if sprite.tag == tag:
            sprite.kill()


# Initial setup
pg.init()
pg.display.set_caption('Nonogram')
screen = pg.display.set_mode((700, 700))
running = True
delta_time = 0.1
clock = pg.time.Clock()
font = pg.font.Font('segoeui.ttf', 18)
start_time = time.time()
elapsed_time = 0
zoom = 1

orig_cross_image = pg.image.load('cross.png').convert_alpha()
orig_cross_image.set_colorkey('white')

mb_pressed = 0  # Mouse button currently being pressed
first_changed_state = None  # State of the box over which the current mouse press began
won = False
grid_name = ''

# Constants
MARGIN_BOTTOMRIGHT = 65
GRID_BG_COL = (190, 190, 190)
LINE_COL = (150, 150, 150)
THICK_LINE_COL = (130, 130, 130)
GRID_BORDER_COL = (10, 10, 10)

# Add event listeners
event_manager = EventManager()
event_manager.add_listener(pg.QUIT, on_quit)
event_manager.add_listener(pg.MOUSEBUTTONDOWN, on_mouse_down)
event_manager.add_listener(pg.MOUSEBUTTONUP, on_mouse_up)
event_manager.add_listener(pg.KEYDOWN, on_key_down)
event_manager.add_listener(pg.MOUSEWHEEL, on_mousewheel)
event_manager.add_listener(pg.MOUSEMOTION, on_mouse_motion)

# UI
sprites = pg.sprite.Group()
sprites.add(Button((75, screen.height - 33), on_load_button_pressed, 'Load grid', event_manager))
sprites.add(Button((210, screen.height - 33), on_random_button_pressed, 'Random grid', event_manager))
sprites.add(Button((365, screen.height - 33), on_solve_button_pressed, 'Show solution', event_manager))

create_random_grid(10)

while running:
    screen.fill(pg.color.Color('white'))
    draw_grid()
    sprites.update()
    sprites.draw(screen)

    # Draw infobar
    screen.fill(GRID_BG_COL, (0, 0, screen.width, 32))
    pg.draw.line(screen, THICK_LINE_COL, (0, 32), (screen.width, 32), 2)

    if won:
        solved_text = font.render('SOLVED', True, GRID_BORDER_COL)
        screen.blit(solved_text, solved_text.get_rect(left=screen.get_rect().left + 8, top=4))

    if not won:
        elapsed_time = time.gmtime(time.time() - start_time)
    elapsed_text = font.render(time.strftime('%M:%S', elapsed_time), True, GRID_BORDER_COL)
    screen.blit(elapsed_text, elapsed_text.get_rect(right=screen.get_rect().right - 8, top=4))

    name_text = font.render(f'{grid_name}  [{grid_size}x{grid_size}]', True, GRID_BORDER_COL)
    screen.blit(name_text, name_text.get_rect(centerx=screen.get_rect().centerx, top=4))

    pg.display.flip()

    # Check if the grid is solved
    if not won:
        if is_grid_solved():
            won = True
            pg.display.message_box('Solved', 'Grid solved!')

    if mb_pressed:
        on_mouse_pressed()

    event_manager.manage_events()

    delta_time = clock.tick(60) / 100
    delta_time = min(1.0, delta_time)

pg.quit()
