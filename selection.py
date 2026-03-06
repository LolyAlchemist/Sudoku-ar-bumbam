
class BombSelect:
    """Two horizontal rows of 1-9 buttons below the sudoku grid for selecting bomb answers.
    Layout: B1-> [1][2][3][4][5][6][7][8][9]
            B2->[1][2][3][4][5][6][7][8][9]
    """

    BTN_W = 80
    BTN_H = 80
    LABEL_W = 100 
    ROW_Y = [730, 820]

    def __init__(self, pygame, font):
        self.pygame = pygame
        self.my_font = font

        self.color_selected = (0, 170, 255)
        self.color_normal = (0, 0, 0)


        self.bomb_answers = [0, 0]
        self.active_bomb = 0 
        self.scroll_offset = 0

    def _row_positions(self, row: int) -> list[tuple]:
        y = self.ROW_Y[row]
        return [(self.LABEL_W + i * self.BTN_W, y) for i in range(9)]

    def draw(self, pygame, surface):
        for bi in range(2):
            y = self.ROW_Y[bi]
            label_color = self.color_selected if bi == self.active_bomb else self.color_normal
            label_text = self.my_font.render(f"B{bi+1}>", False, label_color)
            surface.blit(label_text, (0, y + 15))


            for index, pos in enumerate(self._row_positions(bi)):
                btn_label = str(index + 1)
                pygame.draw.rect(surface, self.color_normal,
                                 [pos[0], pos[1], self.BTN_W, self.BTN_H], width=3, border_radius=10)

                if self._button_hover(pos):
                    pygame.draw.rect(surface, self.color_selected,
                                     [pos[0], pos[1], self.BTN_W, self.BTN_H], width=3, border_radius=10)
                    text_surface = self.my_font.render(btn_label, False, self.color_selected)
                else:
                    text_surface = self.my_font.render(btn_label, False, self.color_normal)

                if self.bomb_answers[bi] == index + 1:
                    pygame.draw.rect(surface, self.color_selected,
                                     [pos[0], pos[1], self.BTN_W, self.BTN_H], width=3, border_radius=10)
                    text_surface = self.my_font.render(btn_label, False, self.color_selected)

                surface.blit(text_surface, (pos[0] + 30, pos[1] + 26))

    def button_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        for bi in range(2):
            for index, pos in enumerate(self._row_positions(bi)):
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
        return pos[0] < mouse_x < pos[0] + self.BTN_W and pos[1] < mouse_y < pos[1] + self.BTN_H

    def reset(self):
        self.bomb_answers = [0, 0]
        self.active_bomb = 0


class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 80
        self.btn_h = 80
        self.my_font = font
        self.selected_number = 0
        self.scroll_offset = 0

        self.color_selected = (0,170,255)
        self.color_normal = (0, 0, 0)

        self.btn_positions = [(800,50), (890,50),
                              (800,150), (890,150),
                              (800,250), (890,250),
                              (800,350), (890,350),
                              (800,450), (890,450)]

        
    
    def draw(self,pygame,surface):
        for index, pos in enumerate(self.btn_positions):
            is_eraser = index == 9
            label = "" if is_eraser else str(index + 1)
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius = 10)

            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius=10)
                text_surface = self.my_font.render(label, False, (0,170,255))
            else:
                text_surface = self.my_font.render(label, False, self.color_normal)

            if not is_eraser and self.selected_number > 0 and self.selected_number - 1 == index:
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius=10)
                text_surface = self.my_font.render(label, False, self.color_selected)

            if is_eraser and self.selected_number == 0:
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius=10)
                text_surface = self.my_font.render(label, False, self.color_selected)

            surface.blit(text_surface, (pos[0] + 30, pos[1] + 26))
    

    def button_clicked(self, mouse_x:int, mouse_y:int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = 0 if index == 9 else index + 1
    



    def button_hover(self, pos: tuple) -> bool|None:
        mx, my = self.pygame.mouse.get_pos()
        if self.on_button(mx, my + self.scroll_offset, pos):
            return True
    
    def on_button(self, mouse_x:int , mouse_y:int, pos:tuple) -> bool:
        return pos[0] < mouse_x < pos[0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h
          
