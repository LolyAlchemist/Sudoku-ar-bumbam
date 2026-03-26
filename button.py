import pygame

class Button():
    def __init__(self, x, y, image, scale, hover_image=None, hover_padding=0):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
        self.hover_image = None
        if hover_image is not None:
            hover_width = hover_image.get_width()
            hover_height = hover_image.get_height()
            self.hover_image = pygame.transform.scale(hover_image, (int(hover_width * scale), int(hover_height * scale)))
        
        self.hover_rect = None
        if hover_padding > 0:
            self.hover_rect = pygame.Rect(
                x + hover_padding,
                y + hover_padding,
                self.rect.width - hover_padding * 2,
                self.rect.height - hover_padding * 2
            )

    def draw(self, surface, mouse_pos=None):
        action = False

        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        hit_rect = self.hover_rect if self.hover_rect is not None else self.rect
        
        if hit_rect.collidepoint(mouse_pos):
            if self.hover_image is not None:
                surface.blit(self.hover_image, (self.rect.x, self.rect.y))
            else:
                surface.blit(self.image, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            self.clicked = False
            surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
