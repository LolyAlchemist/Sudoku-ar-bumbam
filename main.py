import pygame
from scrollbar import ScrollBar
import os
import button
from grid import Grid

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (100, 25)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

# Base resolution for aspect ratio calculation
BASE_WIDTH = 1200
BASE_HEIGHT = 800

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCROLL_HEIGHT = 1400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sudoku ar bumbām")

game_font = pygame.font.SysFont("Arial", 50) 
game_font2 = pygame.font.SysFont("Arial", 25)

grid = Grid(pygame, game_font)

# Load original images (not scaled)
game_bg_orig = pygame.image.load("pics/Untitled46_20260113230129.png").convert()
menu_bg_orig = pygame.image.load("pics/menu.png").convert()
tutorial_bg_orig = pygame.image.load("pics/noteik.png").convert()

# Scaled backgrounds (will be updated on resize)
menu_bg = menu_bg_orig
game_bg = game_bg_orig
tutorial_bg = tutorial_bg_orig

start_img = pygame.image.load("pics/spele.png").convert_alpha()
quit_img = pygame.image.load("pics/iziet.png").convert_alpha()
tuto_img = pygame.image.load("pics/noteikumi.png").convert_alpha()
back_img = pygame.image.load("pics/atpakal.png").convert_alpha()
iesniegt_img = pygame.image.load("pics/iesniegt.png").convert_alpha()
restartet_img = pygame.image.load("pics/restartet1.png").convert_alpha()
iesniegt_hover_img = pygame.image.load("pics/iesniegt_hover.png").convert_alpha()
restartet_hover_img = pygame.image.load("pics/restartet1_hover.png").convert_alpha()

# Scale factor for responsive sizing
current_scale = 1.0

def scale_image(img, scale):
    """Scale an image by the given scale factor"""
    w = int(img.get_width() * scale)
    h = int(img.get_height() * scale)
    return pygame.transform.scale(img, (w, h))

# Buttons with hover images - using scale 2 like original
start_button = button.Button(450, 150, start_img, 2)
quit_button = button.Button(450, 450, quit_img, 2)
tuto_button = button.Button(450, 300, tuto_img, 2)
back_button = button.Button(450, 650, back_img, 2)
game_back_button = button.Button(0, 1020, back_img, 2)

# iesniegt and restartet buttons with hover images
iesniegt_button = button.Button(800, 550, iesniegt_img, 2, iesniegt_hover_img, 20)
restartet_button = button.Button(800, 650, restartet_img, 2, restartet_hover_img, 20)

state = "menu"
run = True

scrollbar = ScrollBar(1150, 0, SCREEN_HEIGHT)
scroll = pygame.Surface((SCREEN_WIDTH, SCROLL_HEIGHT))
scroll_offset = 0

def handle_resize(width, height):
    """Handle window resize events"""
    global current_scale, screen, menu_bg, game_bg, tutorial_bg
    global start_button, quit_button, tuto_button, back_button, game_back_button
    global iesniegt_button, restartet_button, scroll, scrollbar
    
    # Calculate scale factor to fill the screen while maintaining aspect ratio
    scale_x = width / BASE_WIDTH
    scale_y = height / BASE_HEIGHT
    current_scale = max(scale_x, scale_y)  # Use max to fill the screen
    
    # Base button scale (2.0 from original) multiplied by current_scale
    button_scale = 2.0 * current_scale
    
    # Recreate screen with new size
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    
    # Scale backgrounds to fill the screen
    menu_bg = scale_image(menu_bg_orig, current_scale)
    game_bg = scale_image(game_bg_orig, current_scale)
    tutorial_bg = scale_image(tutorial_bg_orig, current_scale)
    
    # Recreate scroll surface with proper size
    scroll = pygame.Surface((width, int(SCROLL_HEIGHT * current_scale)))
    
    # Recreate scrollbar
    scrollbar = ScrollBar(int(1150 * current_scale), 0, height)
    
    # Recreate buttons with scaled images - using original scale 2 as base
    start_button = button.Button(int(450 * current_scale), int(150 * current_scale), start_img, button_scale)
    quit_button = button.Button(int(450 * current_scale), int(450 * current_scale), quit_img, button_scale)
    tuto_button = button.Button(int(450 * current_scale), int(300 * current_scale), tuto_img, button_scale)
    back_button = button.Button(int(450 * current_scale), int(650 * current_scale), back_img, button_scale)
    game_back_button = button.Button(0, int(1020 * current_scale), back_img, button_scale)
    iesniegt_button = button.Button(int(800 * current_scale), int(550 * current_scale), iesniegt_img, button_scale, iesniegt_hover_img, int(20 * current_scale))
    restartet_button = button.Button(int(800 * current_scale), int(650 * current_scale), restartet_img, button_scale, restartet_hover_img, int(20 * current_scale))

while run:
    for event in pygame.event.get():
        # Handle window resize
        if event.type == pygame.VIDEORESIZE:
            handle_resize(event.w, event.h)
        
        # Fullscreen toggle with F11
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
                else:
                    info = pygame.display.Info()
                    pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.RESIZABLE)
        
        scrollbar.handle_event(event)

        if event.type == pygame.QUIT:
            run = False

        if state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                adjusted_y = mouse_y + scroll_offset
                
                iesniegt_clicked = iesniegt_button.rect.collidepoint((mouse_x, mouse_y + scroll_offset))
                restartet_clicked = restartet_button.rect.collidepoint((mouse_x, mouse_y + scroll_offset))
                
                if iesniegt_clicked:
                    if not grid.game_over:
                        grid.submit_answer()
                elif restartet_clicked:
                    if grid.saved_grid is not None:
                        grid.load_saved_game()
                    else:
                        grid.restart()
                    grid.restart_allowed = False
                else:
                    grid.get_mouse_click(mouse_x, adjusted_y)

    scroll_offset = int(scrollbar.scroll_percent * (scroll.get_height() - SCREEN_HEIGHT))

    if state == "menu":
        screen.blit(menu_bg, (0, 0))
        if start_button.draw(screen):
            state = "game"
        if tuto_button.draw(screen):
            state = "tutorial"
        if quit_button.draw(screen):
            run = False


    elif state == "game":
        scroll.blit(game_bg, (0, 0))
        grid.draw_all(pygame, scroll, scroll_offset)
        
        adjusted_mouse = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + scroll_offset)
        iesniegt_button.draw(scroll, adjusted_mouse)
        restartet_button.draw(scroll, adjusted_mouse)

        if grid.game_over:
            grid.restart_allowed = True
            if grid.win:
                won_surface = game_font2.render("Tu uzvarēji!", False, (0, 255, 0))
                scroll.blit(won_surface, (int(800 * current_scale), int(570 * current_scale)))
            else:
                fail_surface = game_font2.render("Kļūda! - viss eksplodēja!", False, (255, 0, 0))
                scroll.blit(fail_surface, (int(800 * current_scale), int(570 * current_scale)))

        if game_back_button.draw(scroll, adjusted_mouse):
            state = "menu"
            grid.save_game()
            start_button.clicked = True
            quit_button.clicked = True
            tuto_button.clicked = True

        screen.blit(scroll, (0, -scroll_offset))
        scrollbar.draw(screen)

    elif state == "tutorial":
        scroll.blit(tutorial_bg, (0, 0))
        y = int(20 * current_scale)
        font = pygame.font.SysFont("Arial", int(25 * current_scale))
        text = [
    "NOTEIKUMI:",
    "* Spēkā ir parastie sudoku noteikumi.",
    "* Spēlē ir fiksēts bumbu skaits (2 bumbas).",
    "* Sudoku laukā ir redzamas bumbu atrašanās vietas.",
    "* Katrai bumbai ir norādīts, vai tā ir B1 vai B2.",
    "",
    "* Pie sudoku lauka ir ievades vieta bumbu ciparam.",
    "* Jāievada skaitlis no 1 līdz 9, kas atbilst bumbas vietai sudoku 3x3 apakšrežģī.",
    "",
    "",
    "ZAUDĒJUMA NOSACĪJUMI:",
    "* Spēle tiek zaudēta, ja nav pareizi ieavadīta vismas 1 bumba, sudoku laukā ir nepareizi ievadīti skaitļi.",
    "",
    "UZVARAS NOSACĪJUMI:",
    "* Spēle tiek uzvarēta, ja visi sudoku lauciņi ir aizpildīti pareizi,"
    " un ir ievadīti pareizie cipari zem abām bumbām."
]


        for line in text:
            surface = font.render(line, True, (0, 0, 0))
            scroll.blit(surface, (int(20 * current_scale), y))
            y += int(35 * current_scale)

        adjusted_mouse_tuto = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + scroll_offset)
        if back_button.draw(scroll, adjusted_mouse_tuto):
            state = "menu"
            start_button.clicked = True
            quit_button.clicked = True
            tuto_button.clicked = True

        screen.blit(scroll, (0, -scroll_offset))
        scrollbar.draw(screen)

    pygame.display.flip()

pygame.quit()
