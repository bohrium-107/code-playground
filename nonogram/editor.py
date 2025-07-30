import pygame as pg
from itertools import groupby
import json
from ui import InputBox, EventManager


class Grid:
    def __init__(self, matrix):
        self.matrix = matrix
        self.row_guides = self._get_row_guides()
        self.col_guides = self._get_col_guides()

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
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            box_rect = (grid_rect.x + j * BOX_LENGTH, grid_rect.y + i * BOX_LENGTH, BOX_LENGTH, BOX_LENGTH)

            if grid.get_box(i, j) == 0:
                pg.draw.rect(screen, GRID_BG_COL, box_rect)
            elif grid.get_box(i, j) == 1:
                pg.draw.rect(screen, GRID_BORDER_COL, box_rect)
            elif grid.get_box(i, j) == 2:
                pg.draw.rect(screen, pg.Color('red'), box_rect)  # TODO: Placeholder

    # Draw grid lines
    for i in range(GRID_SIZE - 1):
        # Vertical line
        pg.draw.line(screen, LINE_COL,
                     (grid_rect.x + (i + 1) * BOX_LENGTH, grid_rect.y),
                     (grid_rect.x + (i + 1) * BOX_LENGTH, grid_rect.y + GRID_SIZE * BOX_LENGTH - 1))
        # Horizontal line
        pg.draw.line(screen, LINE_COL,
                     (grid_rect.x, grid_rect.y + (i + 1) * BOX_LENGTH),
                     (grid_rect.x + GRID_SIZE * BOX_LENGTH - 1, grid_rect.y + (i + 1) * BOX_LENGTH))

    for i in range(4, GRID_SIZE - 1, 5):
        # Vertical thick line
        pg.draw.line(screen, THICK_LINE_COL,
                     (grid_rect.x + (i + 1) * BOX_LENGTH, grid_rect.y),
                     (grid_rect.x + (i + 1) * BOX_LENGTH, grid_rect.y + GRID_SIZE * BOX_LENGTH - 1), 3)
        # Horizontal thick line
        pg.draw.line(screen, THICK_LINE_COL,
                     (grid_rect.x, grid_rect.y + (i + 1) * BOX_LENGTH),
                     (grid_rect.x + GRID_SIZE * BOX_LENGTH - 1, grid_rect.y + (i + 1) * BOX_LENGTH), 3)

    # Draw grid border
    pg.draw.rect(screen, GRID_BORDER_COL,
                 (grid_rect.x, grid_rect.y, BOX_LENGTH * GRID_SIZE, BOX_LENGTH * GRID_SIZE), 3)

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
    if e.key == pg.K_r and len(sprites) == 0:
        kill_sprites_with_tag('inputbox')
        new_inputbox = InputBox(screen.get_rect().center,
                                'Size of the new grid:',
                                lambda: create_empty_grid(int(new_inputbox.text)),
                                event_manager,
                                'inputbox')
        sprites.add(new_inputbox)
    elif e.key == pg.K_s and len(sprites) == 0:
        kill_sprites_with_tag('inputbox')
        new_inputbox = InputBox(screen.get_rect().center,
                                'Save grid as:',
                                lambda: save_grid(new_inputbox.text),
                                event_manager,
                                'inputbox')
        sprites.add(new_inputbox)
    elif e.key == pg.K_l and len(sprites) == 0:
        kill_sprites_with_tag('inputbox')
        new_inputbox = InputBox(screen.get_rect().center,
                                'Name of the grid to load:',
                                lambda: load_grid(new_inputbox.text),
                                event_manager,
                                'inputbox')
        sprites.add(new_inputbox)
    elif e.key == pg.K_ESCAPE:
        kill_sprites_with_tag('inputbox')

def on_mouse_pressed():
    mousex, mousey = pg.mouse.get_pos()
    col_clicked = (mousex - grid_rect.x) / BOX_LENGTH
    row_clicked = (mousey - grid_rect.y) / BOX_LENGTH

    toggle_map = {
        (1, 0): 1,
        (1, 1): 0
    }

    if 0 < col_clicked < GRID_SIZE and 0 < row_clicked < GRID_SIZE:  # if mouse on grid
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
    global BOX_LENGTH, GRID_SIZE, grid, grid_rect, grid_created

    with open(f'grids/{name}.json') as file:
        grid = Grid(json.load(file))

    GRID_SIZE = len(grid.matrix)
    BOX_LENGTH = int((screen.width - MARGIN_BOTTOMRIGHT - MARGIN_TOPLEFT) / GRID_SIZE)
    grid_rect = pg.Rect(MARGIN_TOPLEFT, MARGIN_TOPLEFT, BOX_LENGTH * GRID_SIZE, BOX_LENGTH * GRID_SIZE)
    grid_created = True

def create_empty_grid(size):
    global BOX_LENGTH, GRID_SIZE, grid, grid_rect, grid_created
    GRID_SIZE = size
    BOX_LENGTH = int((screen.width - MARGIN_BOTTOMRIGHT - MARGIN_TOPLEFT) / size)

    grid = Grid([[0] * size for _ in range(size)])
    grid_rect = pg.Rect(MARGIN_TOPLEFT, MARGIN_TOPLEFT, BOX_LENGTH * size, BOX_LENGTH * size)
    grid_created = True

def save_grid(name):
    with open(f'grids/{name}.json', 'w') as file:
        json.dump(grid.matrix, file)

def kill_sprites_with_tag(tag):
    for sprite in sprites:
        if sprite.tag == tag:
            sprite.kill()


# Setup
pg.init()
pg.display.set_caption('Nonogram')
screen = pg.display.set_mode((700, 700))
running = True
delta_time = 0.1
clock = pg.time.Clock()

mb_pressed = 0  # Mouse button currently being pressed
first_changed_state = None  # State of the box over which the current mouse press began
grid_created = False

# Constants
MARGIN_BOTTOMRIGHT = 90
MARGIN_TOPLEFT = 90
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

sprites = pg.sprite.Group()
new_inputbox = InputBox(screen.get_rect().center,
                        'Size of the new grid:',
                        lambda: create_empty_grid(int(new_inputbox.text)),
                        event_manager,
                        'inputbox')
sprites.add(new_inputbox)

while running:
    screen.fill(pg.color.Color('white'))

    if grid_created:
        draw_grid()

    sprites.update()
    sprites.draw(screen)

    screen.blit(pg.Font(None, 25).render(
        'r to create a new grid, s to save grid to a file, l to load a grid from a file, \nESC to close input box',
        True, 'black'), (20, 20))

    if grid_created and mb_pressed:
        on_mouse_pressed()

    delta_time = clock.tick(60) / 100
    delta_time = min(1.0, delta_time)

    event_manager.manage_events()

    pg.display.flip()

pg.quit()
