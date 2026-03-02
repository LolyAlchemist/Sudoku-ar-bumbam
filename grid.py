from random import sample
from selection import SelectNumber
from copy import deepcopy
import random
import os


SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE


def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    points = []
    grid_pixels = cell_size * 9

    for y in range(10):
        points.append([(0, y * cell_size), (grid_pixels, y * cell_size)])

    for x in range(10):
        points.append([(x * cell_size, 0), (x * cell_size, grid_pixels)])

    return points


def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE


def shuffle(samp: range) -> list:
    return sample(samp, len(samp))


def create_grid(sub_grid: int) -> list[list]:
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def remove_numbers(grid: list[list]) -> None:
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * 3 // 30
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0


class Grid:
    def __init__(self, pygame, font):
        self.cell_size = 80
        self.line_coordinates = create_line_coordinates(self.cell_size)

        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)

        self.win = False
        self.restart_allowed = False

        self.game_font = font

        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

        self.selection = SelectNumber(pygame, self.game_font)

        self.bomb_img = pygame.image.load(os.path.join("pics","Untitled45_20260113225822.png")).convert_alpha()
        self.bomb_img = pygame.transform.scale(self.bomb_img, (50, 50))

        self.bombs = []
        self.generate_bombs()

        self.bomb_answers = ["", ""]
        self.bomb_cell_correct = {}
        self.bomb_feedback = ""
        self.bomb_feedback_color = (255, 255, 255)
        self.active_bomb_input = 0

    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

        self.win = False
        self.generate_bombs()
        self.bomb_answers = ["", ""]
        self.bomb_cell_correct.clear()
        self.bomb_feedback = ""

    def check_grids(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        return (y, x) in self.occupied_cell_coordinates

    def get_mouse_click(self, x: int, y: int) -> None:
        if x <= self.cell_size * 9 and y <= self.cell_size * 9:
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            if not self.is_cell_preoccupied(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, self.selection.selected_number)

        self.selection.button_clicked(x, y)

        if self.check_grids():
            self.check_win()

    def pre_occupied_cells(self) -> list[tuple]:
        occupied = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    occupied.append((y, x))
        return occupied

    def __draw_lines(self, pg, surface) -> None:
        for index, point in enumerate(self.line_coordinates):
            color = (0, 0, 0) if index in (3, 6, 13, 16) else (0, 170, 255)
            pg.draw.line(surface, color, point[0], point[1])

    def __draw_numbers(self, surface) -> None:
        for y in range(9):
            for x in range(9):
                cell_value = self.get_cell(x, y)

                center = (
                    x * self.cell_size + self.cell_size // 2,
                    y * self.cell_size + self.cell_size // 2
                )

                if (y, x) in self.bombs:
                    bomb_rect = self.bomb_img.get_rect(center=center)
                    surface.blit(self.bomb_img, bomb_rect)

                    bomb_index = self.bombs.index((y, x))
                    label = self.game_font.render(str(bomb_index + 1), False, (255, 255, 204))
                    label_rect = label.get_rect(center=center)
                    surface.blit(label, label_rect)

                    if (y, x) in self.bomb_cell_correct:
                        correct = self.bomb_cell_correct[(y, x)]
                        entered = self.bomb_answers[bomb_index]
                        if entered and (not correct or self.win):
                            color = (0, 255, 0) if correct else (255, 0, 0)
                            num_surface = self.game_font.render(str(self.__test_grid[y][x]), False, color)
                            surface.blit(num_surface, num_surface.get_rect(center=center))
                    continue

                if cell_value == 0:
                    continue

                if (y, x) in self.occupied_cell_coordinates:
                    color = (0, 0, 0)
                else:
                    color = (0, 51, 102)

                if cell_value != self.__test_grid[y][x]:
                    color = (255, 0, 0)

                text_surface = self.game_font.render(str(cell_value), False, color)
                surface.blit(text_surface, text_surface.get_rect(center=center))

    def generate_bombs(self):
        bombs = []
        used_blocks = set()

        attempts = 0
        while len(bombs) < 2 and attempts < 1000:
            attempts += 1
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            block_id = (row // 3, col // 3)
            if block_id in used_blocks:
                continue

            used_blocks.add(block_id)
            bombs.append((row, col))

        if len(bombs) < 2:
            bombs = [(0, 0), (3, 3)]

        self.bombs = bombs

    def submit_bomb_answer(self):
        self.bomb_cell_correct.clear()

        try:
            entered = [int(a) for a in self.bomb_answers]
        except ValueError:
            self.bomb_feedback = "Ievadiet abus skaitļus!"
            self.bomb_feedback_color = (178, 102, 255)
            return

        correct_count = 0
        for (r, c), value in zip(self.bombs, entered):
            correct = value == self.__test_grid[r][c]
            self.bomb_cell_correct[(r, c)] = correct
            if correct:
                correct_count += 1

        if correct_count == 2:
            self.bomb_feedback = "Abas bombas ir pareizas!"
            self.bomb_feedback_color = (0, 51, 102)
        elif correct_count == 1:
            self.bomb_feedback = "1 pareizs, 1 nepareizs."
            self.bomb_feedback_color = (193, 193, 87)
        else:
            self.bomb_feedback = "Abi nepareizi"
            self.bomb_feedback_color = (109, 208, 125)

        if self.check_grids() and all(self.bomb_cell_correct.get(b, False) for b in self.bombs):
                self.win = True
                self.restart_allowed = True

    def draw_all(self, pg, surface):
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)

        info_font = self.game_font

        grid_pixel_size = self.cell_size * 9
        x = 20
        y = grid_pixel_size + 10

        surface.blit(info_font.render("Bumbas:", False, (0, 0, 0)), (x, y))

        enter_label = "Ievadiet bumbu numurus (TAB, lai pārietu uz otro):"
        enter_label_x = x
        enter_label_y = y + 35
        surface.blit(info_font.render(enter_label, False, (0, 0, 0)),
                    (enter_label_x, enter_label_y))

        label_width, _ = info_font.size(enter_label)
        for i, val in enumerate(self.bomb_answers):
            color = (0, 0, 0) if i == self.active_bomb_input else (0, 51, 102)
            bomb_x = enter_label_x + label_width + 10 + i * 120
            bomb_y = enter_label_y
            surface.blit(info_font.render(f"B{i+1}:{val or '_'}", False, color), (bomb_x, bomb_y))

        if self.bomb_feedback:
            surface.blit(
                info_font.render(self.bomb_feedback, False, self.bomb_feedback_color),
                (x, enter_label_y + 40)
            )


    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        self.grid[y][x] = value

    def check_win(self):
        sudoku_complete = self.check_grids()
        bombs_correct = all(self.bomb_cell_correct.get(b, False) for b in self.bombs)
        self.win = sudoku_complete and bombs_correct
        if self.win:
            self.restart_allowed = True
