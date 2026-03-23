import pygame
from scrollbar import ScrollBar
import os
import button
from grid import Grid

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (100, 25)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCROLL_HEIGHT = 1400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku ar bumbām")

game_font = pygame.font.SysFont("Arial", 50) 
game_font2 = pygame.font.SysFont("Arial", 20)

grid = Grid(pygame, game_font)

game_bg = pygame.image.load("pics/Untitled46_20260113230129.png").convert()
menu_bg = pygame.image.load("pics/menu.png").convert()
tutorial_bg = pygame.image.load("pics/noteik.png").convert()


start_img = pygame.image.load("pics/spele.png").convert_alpha()
quit_img = pygame.image.load("pics/iziet.png").convert_alpha()
tuto_img = pygame.image.load("pics/noteikumi.png").convert_alpha()
back_img = pygame.image.load("pics/atpakal.png").convert_alpha()

start_button = button.Button(450, 150, start_img, 2)
quit_button = button.Button(450, 450, quit_img, 2)
tuto_button = button.Button(450, 300, tuto_img, 2)
back_button = button.Button(450, 650, back_img, 2)
game_back_button = button.Button(0, 1020, back_img, 2)

state = "menu"
run = True

scrollbar = ScrollBar(1150, 0, SCREEN_HEIGHT)
scroll = pygame.Surface((SCREEN_WIDTH, SCROLL_HEIGHT))
scroll_offset = 0

while run:
    for event in pygame.event.get():
        scrollbar.handle_event(event)

        if event.type == pygame.QUIT:
            run = False

        if state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and getattr(grid, "restart_allowed", False):
                    grid.restart()
                    grid.restart_allowed = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                adjusted_mouse_y = mouse_y + scroll_offset
                grid.get_mouse_click(mouse_x, adjusted_mouse_y)

    scroll_offset = int(scrollbar.scroll_percent * (SCROLL_HEIGHT - SCREEN_HEIGHT))

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

        sudoku_complete = grid.check_grids()
        bombs_correct = all(grid.bomb_cell_correct.get(b, False) for b in grid.bombs)
        bombs_wrong = any(bomb in grid.bomb_cell_correct and not grid.bomb_cell_correct[bomb] for bomb in grid.bombs)

        grid.restart_allowed = False

        if grid.game_over:
            grid.restart_allowed = True
            if grid.win:
                won_surface = game_font2.render("Tu uzvarēji!", False, (0, 255, 0))
                press_space_surf = game_font2.render("Spied space, lai restartētu.", False, (0, 255, 200))
                scroll.blit(won_surface, (0, 960))
                scroll.blit(press_space_surf, (0, 985))
            else:
                fail_surface = game_font2.render("Kļūda! Restartē.", False, (255, 0, 0))
                press_space_surf = game_font2.render("Spied space, lai restartētu.", False, (255, 80, 80))
                scroll.blit(fail_surface, (0, 960))
                scroll.blit(press_space_surf, (0, 985))

        adjusted_mouse = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + scroll_offset)
        if game_back_button.draw(scroll, adjusted_mouse):
            state = "menu"
            grid.restart()
            start_button.clicked = True
            quit_button.clicked = True
            tuto_button.clicked = True

        screen.blit(scroll, (0, -scroll_offset))
        scrollbar.draw(screen)

    elif state == "tutorial":
        scroll.blit(tutorial_bg, (0, 0))
        y = 20
        font = pygame.font.SysFont("Arial", 25)
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
            scroll.blit(surface, (20, y))
            y += 35

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
