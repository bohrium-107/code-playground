import pygame as pg
from itertools import groupby


class Grid:
    def __init__(self, matrix):
        self._matrix = matrix
        self.row_guides = self._get_row_guides()
        self.col_guides = self._get_col_guides()

    # Returns a list of lists of numbers representing the consecutive black boxes in each row
    def _get_row_guides(self):
        guides = []

        for i in range(len(self._matrix)):
            guides.append([len(list(group)) for key, group in groupby(self.get_row(i)) if key == 1])

        return guides

    # Returns a list of lists of numbers representing the consecutive black boxes in each column
    def _get_col_guides(self):
        guides = []

        for i in range(len(self._matrix)):
            guides.append([len(list(group)) for key, group in groupby(self.get_col(i)) if key == 1])

        return guides

    # Returns the i-th column
    def get_col(self, i):
        return list(map(lambda row: row[i], self._matrix))

    # Returns the i-th row
    def get_row(self, i):
        return self._matrix[i]

    # Get the state of a box
    def get_box(self, row, col):
        return self._matrix[row][col]

    # Set the state of a box
    def set_box(self, row, col, state):
        self._matrix[row][col] = state
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

    # Draw guides
    font = pg.font.Font(None, 30)
    spacing_hor = 23
    spacing_vert = 27
    # correct_rows = get_correct_rows()
    # correct_cols = get_correct_cols()

    for i in range(GRID_SIZE):
        nums = solution.row_guides[i]
        # Check if the boxes on the current grid row match the guides
        text_color = pg.Color('dark gray') if nums == grid.row_guides[i] else pg.Color('black')

        for j in range(len(nums)):
            text = str(nums[-1 - j])
            text_surf = font.render(text, True, text_color)
            text_rect = text_surf.get_rect(right=grid_rect.left - 15 - j * spacing_hor,
                                           centery=grid_rect.top + BOX_LENGTH / 2 + i * BOX_LENGTH)
            screen.blit(text_surf, text_rect)

    for i in range(GRID_SIZE):
        nums = solution.col_guides[i]
        # Check if the boxes on the current grid col match the guides
        text_color = pg.Color('dark gray') if nums == grid.col_guides[i] else pg.Color('black')

        for j in range(len(nums)):
            text = str(nums[-1 - j])
            text_surf = font.render(text, True, text_color)
            text_rect = text_surf.get_rect(bottom=grid_rect.top - 10 - j * spacing_vert,
                                           centerx=grid_rect.left + BOX_LENGTH / 2 + i * BOX_LENGTH)
            screen.blit(text_surf, text_rect)

# def get_correct_rows():
#     result = [False] * GRID_SIZE
#     for row in range(GRID_SIZE):
#         result[row] = row_guides[0] == list(
#             map(lambda x: len(list(x[1])), filter(lambda x: x[0] == 1, groupby(grid[row]))))
#
#     return result
#
# def get_correct_cols():
#     result = [False] * GRID_SIZE
#     for col in range(GRID_SIZE):
#         grid_col = list(map(lambda x: x[col], grid))
#         result[col] = col_guides[0] == list(
#             map(lambda x: len(list(x[1])), filter(lambda x: x[0] == 1, groupby(grid_col))))
#
#     return result

def on_mouse_down(e):
    global pressed, first_changed_state
    pressed = e.button

def on_mouse_up():
    global pressed, first_changed_state
    pressed = 0
    first_changed_state = None
    # changed_boxes.clear()

def on_mouse_pressed():
    mousex, mousey = pg.mouse.get_pos()
    col_clicked = (mousex - grid_rect.x) / BOX_LENGTH
    row_clicked = (mousey - grid_rect.y) / BOX_LENGTH

    toggle_map = {
        (1, 0): 1,
        (1, 1): 0,
        (3, 0): 2,
        (3, 2): 0,
    }

    if 0 < col_clicked < GRID_SIZE and 0 < row_clicked < GRID_SIZE:  # if mouse on grid
        row = int(row_clicked)
        col = int(col_clicked)
        box_state = grid.get_box(row, col)

        global first_changed_state
        if first_changed_state is None:
            first_changed_state = box_state

        # Only change state if this box has the same state as the box changed first with this mouse press
        # if (pressed, box_state) in toggle_map and (row, col) not in changed_boxes and box_state == first_changed_state:
        if (pressed, box_state) in toggle_map and box_state == first_changed_state:
            grid.set_box(row, col, toggle_map[(pressed, box_state)])
            # changed_boxes.append((row, col))


# # Returns two lists: one for row guides and one for column guides
# def get_guides(solution):
#     row_guides = [[] for _ in range(GRID_SIZE)]
#     col_guides = [[] for _ in range(GRID_SIZE)]
#
#     for row in range(GRID_SIZE):
#         streak = 0
#
#         for box in solution[row]:
#             if box == 0 and streak != 0:
#                 row_guides[row].append(streak)
#                 streak = 0
#             elif box == 1:
#                 streak += 1
#
#         if streak != 0 or not row_guides[row]:
#             row_guides[row].append(streak)
#
#     for col in range(GRID_SIZE):
#         streak = 0
#
#         for box in map(lambda x: x[col], solution):
#             if box == 0 and streak != 0:
#                 col_guides[col].append(streak)
#                 streak = 0
#             elif box == 1:
#                 streak += 1
#
#         if streak != 0 or not col_guides[col]:
#             col_guides[col].append(streak)
#
#     return row_guides, col_guides


# Setup
pg.init()
pg.display.set_caption('Nonogram')
screen = pg.display.set_mode((700, 700))
running = True
delta_time = 0.1
clock = pg.time.Clock()

GRID_SIZE = 10
MARGIN_BOTTOMRIGHT = 50
MARGIN_TOPLEFT = 150
BOX_LENGTH = int((screen.width - MARGIN_BOTTOMRIGHT - MARGIN_TOPLEFT) / GRID_SIZE)

grid = Grid([[0] * GRID_SIZE for _ in range(GRID_SIZE)])
solution = Grid([[1, 0, 0, 1, 1, 1, 1, 0, 1, 1],
                 [1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                 [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                 [0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 1],
                 [0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
                 [0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                 [0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 ])

pressed = 0  # Mouse button currently being pressed
first_changed_state = None  # State of the box over which the current mouse press began
# changed_boxes = []  # Boxes hovered over during the current mouse press

grid_rect = pg.Rect(MARGIN_TOPLEFT, MARGIN_TOPLEFT, BOX_LENGTH * GRID_SIZE, BOX_LENGTH * GRID_SIZE)

# Colors
GRID_BG_COL = (190, 190, 190)
LINE_COL = (150, 150, 150)
THICK_LINE_COL = (130, 130, 130)
GRID_BORDER_COL = (10, 10, 10)

while running:
    screen.fill(pg.color.Color('white'))
    draw_grid()

    pg.display.flip()

    delta_time = clock.tick(60) / 100
    delta_time = min(1.0, delta_time)

    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            on_mouse_down(event)
        elif event.type == pg.MOUSEBUTTONUP:
            on_mouse_up()

    if pressed:
        on_mouse_pressed()

pg.quit()
