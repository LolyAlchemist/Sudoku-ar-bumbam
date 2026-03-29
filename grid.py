from random import sample
from selection import SelectNumber, BombSelect
from copy import deepcopy
import random
import os
from typing import Optional


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
    return (
        SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num
    ) % GRID_SIZE


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
    empties = num_of_cells * 3 // 25
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0


class Grid:
    def __init__(self, pygame, font):
        self.cell_size = 80
        self.line_coordinates = create_line_coordinates(self.cell_size)

        self.grid: list[list[int]] = create_grid(SUB_GRID_SIZE)
        self.__test_grid: list[list[int]] = deepcopy(self.grid)

        self.win = False
        self.restart_allowed = False
        self.game_over = False

        self.game_font = font

        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

        self.selection = SelectNumber(pygame, self.game_font)
        self.bomb_select = BombSelect(pygame, self.game_font)

        self.bomb_img = pygame.image.load(
            os.path.join("pics", "Untitled45_20260113225822.png")
        ).convert_alpha()
        self.bomb_img = pygame.transform.scale(self.bomb_img, (50, 50))

        self.bombs = []
        self.generate_bombs()

        self.bomb_cell_correct = {}
        self.bomb_feedback = ""
        self.bomb_feedback_color = (255, 255, 255)

        self.saved_grid = None
        self.saved_test_grid = None
        self.saved_bombs = None
        self.saved_occupied = None
        self.saved_bomb_answers = None
        self.saved_selection_number = 0

    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

        self.win = False
        self.game_over = False
        self.generate_bombs()
        self.bomb_select.reset()
        self.bomb_cell_correct.clear()
        self.bomb_feedback = ""
        self.saved_grid = None
        self.saved_test_grid = None
        self.saved_bombs = None
        self.saved_occupied = None
        self.saved_bomb_answers = None

    def check_grids(self):
        bomb_set = set(self.bombs)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (y, x) in bomb_set:
                    continue
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        return (y, x) in self.occupied_cell_coordinates

    def is_grid_full(self) -> bool:
        bomb_set = set(self.bombs)
        for row in range(9):
            for col in range(9):
                if (row, col) not in bomb_set and self.grid[row][col] == 0:
                    return False
        return True

    def get_mouse_click(self, x: int, y: int) -> None:
        if self.game_over:
            return

        if x <= self.cell_size * 9 and y <= self.cell_size * 9:
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            if not self.is_cell_preoccupied(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, self.selection.selected_number)

        self.selection.button_clicked(x, y)

        bomb_both_set = self.bomb_select.button_clicked(x, y)

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
                    y * self.cell_size + self.cell_size // 2,
                )

                if (y, x) in self.bombs:
                    bomb_rect = self.bomb_img.get_rect(center=center)
                    surface.blit(self.bomb_img, bomb_rect)

                    bomb_index = self.bombs.index((y, x))
                    label = self.game_font.render(
                        str(bomb_index + 1), False, (255, 255, 204)
                    )
                    label_rect = label.get_rect(center=center)
                    surface.blit(label, label_rect)

                    if (y, x) in self.bomb_cell_correct:
                        correct = self.bomb_cell_correct[(y, x)]
                        entered = self.bomb_select.bomb_answers[bomb_index]
                        if entered and (not correct or self.win):
                            color = (0, 255, 0) if correct else (255, 0, 0)
                            num_surface = self.game_font.render(
                                str(self.__test_grid[y][x]), False, color
                            )
                            surface.blit(
                                num_surface, num_surface.get_rect(center=center)
                            )
                    continue

                if cell_value == 0:
                    continue

                if (y, x) in self.occupied_cell_coordinates:
                    color = (0, 0, 0)
                else:
                    color = (0, 51, 102)

                if (
                    self.game_over
                    and cell_value != self.__test_grid[y][x]
                    and not self.win
                ):
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

        entered = self.bomb_select.bomb_answers
        if 0 in entered:
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

        if self.check_grids() and all(
            self.bomb_cell_correct.get(b, False) for b in self.bombs
        ):
            self.win = True
            self.restart_allowed = True

    def draw_all(self, pg, surface, scroll_offset: int = 0):
        self.selection.scroll_offset = scroll_offset
        self.bomb_select.scroll_offset = scroll_offset
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)
        self.bomb_select.draw(pg, surface)

        if self.bomb_feedback:
            feedback_font = pg.font.SysFont("Arial", 25)
            surface.blit(
                feedback_font.render(
                    self.bomb_feedback, False, self.bomb_feedback_color
                ),
                (800, 520),
            )

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        self.grid[y][x] = value

    def submit_answer(self):
        """Submit answer via iesniegt button - check if all is correct"""
        if not self.is_grid_full():
            self.bomb_feedback = "Aizpildi visus lauciņus!"
            self.bomb_feedback_color = (178, 102, 255)
            return

        if (
            self.bomb_select.bomb_answers[0] == 0
            or self.bomb_select.bomb_answers[1] == 0
        ):
            self.bomb_feedback = "Ievadi abus bombu ciparus!"
            self.bomb_feedback_color = (178, 102, 255)
            return

        self.submit_bomb_answer()

        sudoku_complete = self.check_grids()
        bombs_correct = all(self.bomb_cell_correct.get(b, False) for b in self.bombs)

        self.win = sudoku_complete and bombs_correct
        self.game_over = True
        self.restart_allowed = True

        self.bomb_feedback = ""

    def save_game(self):
        """Save current game state when going back to menu"""
        self.saved_grid = deepcopy(self.grid)
        self.saved_test_grid = deepcopy(self.__test_grid)
        self.saved_bombs = self.bombs.copy()
        self.saved_occupied = self.occupied_cell_coordinates.copy()
        self.saved_bomb_answers = self.bomb_select.bomb_answers.copy()
        self.saved_selection_number = self.selection.selected_number

    def load_saved_game(self):
        """Load saved game when restarting with restartet button"""
        if self.saved_grid is not None:
            saved_grid = self.saved_grid
            saved_test_grid = self.saved_test_grid
            saved_bombs = self.saved_bombs
            saved_occupied = self.saved_occupied
            saved_bomb_answers = self.saved_bomb_answers

            assert saved_test_grid is not None
            assert saved_bombs is not None
            assert saved_occupied is not None
            assert saved_bomb_answers is not None

            self.grid = deepcopy(saved_grid)
            self.__test_grid = deepcopy(saved_test_grid)
            self.bombs = saved_bombs.copy()
            self.occupied_cell_coordinates = saved_occupied.copy()
            self.bomb_select.bomb_answers = saved_bomb_answers.copy()
            self.selection.selected_number = self.saved_selection_number

            self.win = False
            self.game_over = False
            self.bomb_cell_correct.clear()
            self.bomb_feedback = ""
