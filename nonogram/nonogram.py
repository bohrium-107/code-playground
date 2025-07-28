import json
import pygame as pg
from itertools import groupby
from globals import EventManager

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
            box_rect = (grid.rect.x + j * box_length, grid.rect.y + i * box_length, box_length, box_length)

            if grid.get_box(i, j) == 0:
                pg.draw.rect(screen, GRID_BG_COL, box_rect)
            elif grid.get_box(i, j) == 1:
                pg.draw.rect(screen, GRID_BORDER_COL, box_rect)
            elif grid.get_box(i, j) == 2:
                pg.draw.rect(screen, pg.Color('red'), box_rect)  # TODO: Placeholder

    # Draw grid lines
    for i in range(grid_size - 1):
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
    font = pg.font.Font(None, 600 // (grid_size + 10))
    spacing_hor = 23
    spacing_vert = 27

    for i in range(grid_size):
        nums = solution.row_guides[i]
        # If this row matches the solution guides, color the guides gray
        text_color = pg.Color('dark gray') if nums == grid.row_guides[i] else pg.Color('black')

        for j in range(len(nums)):
            text = str(nums[-1 - j])
            text_surf = font.render(text, True, text_color)
            text_rect = text_surf.get_rect(right=grid.rect.left - 15 - j * spacing_hor,
                                           centery=grid.rect.top + box_length / 2 + i * box_length)
            screen.blit(text_surf, text_rect)

    for i in range(grid_size):
        nums = solution.col_guides[i]
        # If this column matches the solution guides, color the guides gray
        text_color = pg.Color('dark gray') if nums == grid.col_guides[i] else pg.Color('black')

        for j in range(len(nums)):
            text = str(nums[-1 - j])
            text_surf = font.render(text, True, text_color)
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
    global pressed
    pressed = e.button

def on_mouse_up(e):
    global pressed, first_changed_state
    pressed = 0
    first_changed_state = None

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
        if (pressed, box_state) in toggle_map and box_state == first_changed_state:
            grid.set_box(row, col, toggle_map[(pressed, box_state)])

def load_grid(name):
    global grid, solution, grid_size, box_length, margin_topleft

    with open(f'grids/{name}.json') as file:
        solution = Grid(json.load(file))

    grid_size = len(solution.matrix)
    margin_topleft = -5250 // (grid_size - 45)
    box_length = int((screen.width - MARGIN_BOTTOMRIGHT - margin_topleft) / grid_size)
    grid = Grid([[0] * grid_size for _ in range(grid_size)],
                pg.Rect(margin_topleft, margin_topleft, box_length * grid_size, box_length * grid_size))

# Initial setup
pg.init()
pg.display.set_caption('Nonogram')
screen = pg.display.set_mode((700, 700))
running = True
delta_time = 0.1
clock = pg.time.Clock()

pressed = 0  # Mouse button currently being pressed
first_changed_state = None  # State of the box over which the current mouse press began
won = False

# Constants
MARGIN_BOTTOMRIGHT = 50
GRID_BG_COL = (190, 190, 190)
LINE_COL = (150, 150, 150)
THICK_LINE_COL = (130, 130, 130)
GRID_BORDER_COL = (10, 10, 10)

# Add event listeners
event_manager = EventManager()
event_manager.add_listener(pg.QUIT, on_quit)
event_manager.add_listener(pg.MOUSEBUTTONDOWN, on_mouse_down)
event_manager.add_listener(pg.MOUSEBUTTONUP, on_mouse_up)

load_grid('apple')

while running:
    screen.fill(pg.color.Color('white'))
    draw_grid()
    pg.display.flip()

    # Check if the grid is solved
    if not won:
        if is_grid_solved():
            won = True
            pg.display.message_box('Solved', 'Grid solved!')  # TODO: Placeholder

    if pressed:
        on_mouse_pressed()

    event_manager.manage_events()

    delta_time = clock.tick(60) / 100
    delta_time = min(1.0, delta_time)

pg.quit()
