class BombSelect:
    """Two horizontal rows of 1-9 buttons below the sudoku grid for selecting bomb answers.
    Layout: B1-> [1][2][3][4][5][6][7][8][9]
            B2->[1][2][3][4][5][6][7][8][9]
    """

    def __init__(self, pygame, font):
        self.pygame = pygame
        self.my_font = font

        self.color_selected = (0, 170, 255)
        self.color_normal = (0, 0, 0)

        self.bomb_answers = [0, 0]
        self.active_bomb = 0
        self.scroll_offset = 0

        self.surface_width = 1200
        self.surface_height = 1000

        self.BTN_W = 80
        self.BTN_H = 80
        self.LABEL_W = 100
        self.ROW_Y = [780, 870]

    def _row_positions(self, row: int, surface_width: int) -> list[tuple]:
        base_y_positions = [780, 870]
        scale = surface_width / 1200
        grid_width = 9 * int(80 * scale)
        start_x = int(100 * scale)
        y = int(base_y_positions[row] * scale)
        return [(start_x + i * int(80 * scale), y) for i in range(9)]

    def draw(self, pygame, surface):
        surface_width = surface.get_width()
        self.surface_width = surface_width
        scale = surface_width / 1200
        self.BTN_W = int(80 * scale)
        self.BTN_H = int(80 * scale)
        self.LABEL_W = int(100 * scale)

        base_y_positions = [780, 870]
        for bi in range(2):
            y = int(base_y_positions[bi] * scale)
            label_color = (
                self.color_selected if bi == self.active_bomb else self.color_normal
            )
            label_text = self.my_font.render(f"B{bi + 1}>", False, label_color)

            surface.blit(label_text, (int(20 * scale), y + int(15 * scale)))

            for index, pos in enumerate(self._row_positions(bi, surface_width)):
                btn_label = str(index + 1)
                pygame.draw.rect(
                    surface,
                    self.color_normal,
                    [pos[0], pos[1], self.BTN_W, self.BTN_H],
                    width=3,
                    border_radius=10,
                )

                if self._button_hover(pos):
                    pygame.draw.rect(
                        surface,
                        self.color_selected,
                        [pos[0], pos[1], self.BTN_W, self.BTN_H],
                        width=3,
                        border_radius=10,
                    )
                    text_surface = self.my_font.render(
                        btn_label, False, self.color_selected
                    )
                else:
                    text_surface = self.my_font.render(
                        btn_label, False, self.color_normal
                    )

                if self.bomb_answers[bi] == index + 1:
                    pygame.draw.rect(
                        surface,
                        self.color_selected,
                        [pos[0], pos[1], self.BTN_W, self.BTN_H],
                        width=3,
                        border_radius=10,
                    )
                    text_surface = self.my_font.render(
                        btn_label, False, self.color_selected
                    )

                surface.blit(
                    text_surface,
                    (pos[0] + self.BTN_W // 2 - 10, pos[1] + self.BTN_H // 2 - 15),
                )

    def button_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        for bi in range(2):
            for index, pos in enumerate(self._row_positions(bi, self.surface_width)):
                if self._on_button(mouse_x, mouse_y, pos):
                    self.bomb_answers[bi] = index + 1
                    self.active_bomb = 1 - bi
                    return self.bomb_answers[0] != 0 and self.bomb_answers[1] != 0
        return False

    def _button_hover(self, pos: tuple) -> bool | None:
        mx, my = self.pygame.mouse.get_pos()
        if self._on_button(mx, my + self.scroll_offset, pos):
            return True

    def _on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        return (
            pos[0] < mouse_x < pos[0] + self.BTN_W
            and pos[1] < mouse_y < pos[1] + self.BTN_H
        )

    def reset(self):
        self.bomb_answers = [0, 0]
        self.active_bomb = 0

    def update_scale(self, scale_factor, pygame_ref, font):
        """Update all scaled elements when window is resized"""
        self.BTN_W = int(80 * scale_factor)
        self.BTN_H = int(80 * scale_factor)
        self.LABEL_W = int(100 * scale_factor)
        self.ROW_Y = [int(730 * scale_factor), int(820 * scale_factor)]
        self.my_font = font
        self.pygame = pygame_ref


class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 80
        self.btn_h = 80
        self.my_font = font
        self.selected_number = 0
        self.scroll_offset = 0

        self.color_selected = (0, 170, 255)
        self.color_normal = (0, 0, 0)

        self.surface_width = 1200

    def _calc_positions(self, surface_width: int) -> list[tuple]:
        grid_width = 2 * self.btn_w + 90
        start_x = (surface_width - grid_width) // 2 + 800 - (surface_width - 1200) // 2
        start_x = int(800 * (surface_width / 1200))
        return [
            (start_x, int(50 * (surface_width / 1200))),
            (
                start_x + int(90 * (surface_width / 1200)),
                int(50 * (surface_width / 1200)),
            ),
            (start_x, int(150 * (surface_width / 1200))),
            (
                start_x + int(90 * (surface_width / 1200)),
                int(150 * (surface_width / 1200)),
            ),
            (start_x, int(250 * (surface_width / 1200))),
            (
                start_x + int(90 * (surface_width / 1200)),
                int(250 * (surface_width / 1200)),
            ),
            (start_x, int(350 * (surface_width / 1200))),
            (
                start_x + int(90 * (surface_width / 1200)),
                int(350 * (surface_width / 1200)),
            ),
            (start_x, int(450 * (surface_width / 1200))),
            (
                start_x + int(90 * (surface_width / 1200)),
                int(450 * (surface_width / 1200)),
            ),
        ]

    def draw(self, pygame, surface):
        surface_width = surface.get_width()
        self.surface_width = surface_width
        self.btn_positions = self._calc_positions(surface_width)
        self.btn_w = int(80 * (surface_width / 1200))
        self.btn_h = int(80 * (surface_width / 1200))

        for index, pos in enumerate(self.btn_positions):
            is_eraser = index == 9
            label = "" if is_eraser else str(index + 1)
            pygame.draw.rect(
                surface,
                self.color_normal,
                [pos[0], pos[1], self.btn_w, self.btn_h],
                width=3,
                border_radius=10,
            )

            if self.button_hover(pos):
                pygame.draw.rect(
                    surface,
                    self.color_selected,
                    [pos[0], pos[1], self.btn_w, self.btn_h],
                    width=3,
                    border_radius=10,
                )
                text_surface = self.my_font.render(label, False, (0, 170, 255))
            else:
                text_surface = self.my_font.render(label, False, self.color_normal)

            if (
                not is_eraser
                and self.selected_number > 0
                and self.selected_number - 1 == index
            ):
                pygame.draw.rect(
                    surface,
                    self.color_selected,
                    [pos[0], pos[1], self.btn_w, self.btn_h],
                    width=3,
                    border_radius=10,
                )
                text_surface = self.my_font.render(label, False, self.color_selected)

            if is_eraser and self.selected_number == 0:
                pygame.draw.rect(
                    surface,
                    self.color_selected,
                    [pos[0], pos[1], self.btn_w, self.btn_h],
                    width=3,
                    border_radius=10,
                )
                text_surface = self.my_font.render(label, False, self.color_selected)

            surface.blit(
                text_surface,
                (pos[0] + self.btn_w // 2 - 10, pos[1] + self.btn_h // 2 - 15),
            )

    def button_clicked(self, mouse_x: int, mouse_y: int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = 0 if index == 9 else index + 1

    def button_hover(self, pos: tuple) -> bool | None:
        mx, my = self.pygame.mouse.get_pos()
        if self.on_button(mx, my + self.scroll_offset, pos):
            return True

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        return (
            pos[0] < mouse_x < pos[0] + self.btn_w
            and pos[1] < mouse_y < pos[1] + self.btn_h
        )

    def update_scale(self, scale_factor, pygame_ref, font):
        """Update all scaled elements when window is resized"""
        self.btn_w = int(80 * scale_factor)
        self.btn_h = int(80 * scale_factor)
        self.my_font = font
        self.pygame = pygame_ref
        self.btn_positions = [
            (int(800 * scale_factor), int(50 * scale_factor)),
            (int(890 * scale_factor), int(50 * scale_factor)),
            (int(800 * scale_factor), int(150 * scale_factor)),
            (int(890 * scale_factor), int(150 * scale_factor)),
            (int(800 * scale_factor), int(250 * scale_factor)),
            (int(890 * scale_factor), int(250 * scale_factor)),
            (int(800 * scale_factor), int(350 * scale_factor)),
            (int(890 * scale_factor), int(350 * scale_factor)),
            (int(800 * scale_factor), int(450 * scale_factor)),
            (int(890 * scale_factor), int(450 * scale_factor)),
        ]
