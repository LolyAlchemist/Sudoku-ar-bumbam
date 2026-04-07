import pygame


class ScrollBar:
    def __init__(self, x, y, h, thumb_h=120, thumb_color=(0, 0, 0), scale_factor=1.0):
        self.x = x
        self.y = y
        self.h = h
        self.w = int(20 * scale_factor)

        self.base_thumb_h = 120
        self.thumb_h = int(thumb_h * scale_factor)
        self.thumb_y = y

        self.thumb_color = thumb_color

        self.dragging = False
        self.scroll_percent = 0

    def update_scale(self, scale_factor):
        self.w = int(20 * scale_factor)
        self.thumb_h = int(self.base_thumb_h * scale_factor)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if (
                self.x <= mx <= self.x + self.w
                and self.thumb_y <= my <= self.thumb_y + self.thumb_h
            ):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.thumb_y = max(
                self.y, min(my - self.thumb_h // 2, self.y + self.h - self.thumb_h)
            )
            self.scroll_percent = (self.thumb_y - self.y) / (self.h - self.thumb_h)

        if event.type == pygame.MOUSEWHEEL:
            scroll_step = 30
            self.thumb_y = max(
                self.y,
                min(
                    self.thumb_y - event.y * scroll_step, self.y + self.h - self.thumb_h
                ),
            )
            self.scroll_percent = (self.thumb_y - self.y) / (self.h - self.thumb_h)

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.thumb_color, (self.x, self.thumb_y, self.w, self.thumb_h)
        )
