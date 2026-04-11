import pygame
from scrollbar import ScrollBar
import os
import button
from grid import Grid

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (100, 25)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

BASE_WIDTH = 1200
BASE_HEIGHT = 800
BASE_SCROLL_HEIGHT = 1400

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCROLL_HEIGHT = 1400

current_scale = 1.0
scroll_height_scaled = BASE_SCROLL_HEIGHT
game_offset_x = 0
game_offset_y = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sudoku ar bumbām")

game_font = pygame.font.SysFont("Arial", 50)
game_font2 = pygame.font.SysFont("Arial", 25)

grid = Grid(pygame, game_font, 1.0)

game_bg_orig = pygame.image.load("pics/Untitled46_20260113230129.png").convert()
menu_bg_orig = pygame.image.load("pics/menu.png").convert()
tutorial_bg_orig = pygame.image.load("pics/noteik.png").convert()

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

current_scale = 1.0


def draw_tiled_bg(surface, bg_image):
    """Draw background image tiled to cover the surface"""
    bg_w = bg_image.get_width()
    bg_h = bg_image.get_height()
    surf_w = surface.get_width()
    surf_h = surface.get_height()

    for y in range(0, surf_h, bg_h):
        for x in range(0, surf_w, bg_w):
            surface.blit(bg_image, (x, y))


start_button = button.Button(450, 150, start_img, 2)
quit_button = button.Button(450, 450, quit_img, 2)
tuto_button = button.Button(450, 300, tuto_img, 2)
back_button = button.Button(450, 650, back_img, 2)
game_back_button = button.Button(100, 950, back_img, 2)

iesniegt_button = button.Button(800, 530, iesniegt_img, 1.4, iesniegt_hover_img, 26)
restartet_button = button.Button(800, 660, restartet_img, 1.4, restartet_hover_img, 26)

state = "menu"
state_changed = True
run = True

scrollbar = ScrollBar(1150, 0, SCREEN_HEIGHT, 120, (0, 0, 0), 1.0)
scroll = pygame.Surface((SCREEN_WIDTH, int(1000 * current_scale)))
scroll_offset = 0


def handle_resize(width, height):
    """Handle window resize events"""
    global current_scale, screen, menu_bg, game_bg, tutorial_bg
    global start_button, quit_button, tuto_button, back_button, game_back_button
    global iesniegt_button, restartet_button, scroll, scrollbar
    global game_font, game_font2

    scale_x = width / BASE_WIDTH
    scale_y = height / BASE_HEIGHT

    # Add 5% safety margin to avoid needing scrollbar when almost fits
    current_scale = min(scale_x, scale_y * 0.95)

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    game_font = pygame.font.SysFont("Arial", int(50 * current_scale))
    game_font2 = pygame.font.SysFont("Arial", int(25 * current_scale))

    grid.update_scale(current_scale, pygame, game_font)

    button_scale = 2.0 * current_scale
    buttons_total_width = start_img.get_width() * button_scale
    center_x = (width - buttons_total_width) // 2

    start_button = button.Button(
        center_x, int(150 * current_scale), start_img, button_scale
    )
    quit_button = button.Button(
        center_x, int(450 * current_scale), quit_img, button_scale
    )
    tuto_button = button.Button(
        center_x, int(300 * current_scale), tuto_img, button_scale
    )
    back_button = button.Button(
        int(450 * current_scale), int(650 * current_scale), back_img, button_scale
    )
    game_back_button = button.Button(
        int(100 * current_scale), int(950 * current_scale), back_img, button_scale
    )
    small_button_scale = 1.4 * current_scale
    iesniegt_button = button.Button(
        int(800 * current_scale),
        int(530 * current_scale),
        iesniegt_img,
        small_button_scale,
        iesniegt_hover_img,
        int(26 * current_scale),
    )
    restartet_button = button.Button(
        int(800 * current_scale),
        int(660 * current_scale),
        restartet_img,
        small_button_scale,
        restartet_hover_img,
        int(26 * current_scale),
    )

    max_scroll_height = int(1080 * current_scale)
    scroll = pygame.Surface((width, max_scroll_height))

    scrollbar = ScrollBar(
        width - int(40 * current_scale),
        0,
        height,
        int(120 * current_scale),
        (0, 0, 0),
        current_scale,
    )


while run:
    next_state = None

    if state_changed:
        scrollbar.scroll_percent = 0
        scrollbar.thumb_y = scrollbar.y
        scroll_offset = 0
        state_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            continue

        if event.type == pygame.VIDEORESIZE:
            handle_resize(event.w, event.h)
            pygame.display.flip()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                surface = pygame.display.get_surface()
                if surface and surface.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
                    handle_resize(BASE_WIDTH, BASE_HEIGHT)
                else:
                    info = pygame.display.Info()
                    pygame.display.set_mode(
                        (info.current_w, info.current_h),
                        pygame.FULLSCREEN | pygame.RESIZABLE,
                    )
                    handle_resize(info.current_w, info.current_h)

        scrollbar.handle_event(event)

        if state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                adjusted_y = mouse_y + scroll_offset

                iesniegt_clicked = iesniegt_button.rect.collidepoint(
                    (mouse_x, mouse_y + scroll_offset)
                )
                restartet_clicked = restartet_button.rect.collidepoint(
                    (mouse_x, mouse_y + scroll_offset)
                )

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

    if not run:
        break

    scroll_offset = int(
        scrollbar.scroll_percent * max(0, scroll.get_height() - screen.get_height())
    )

    if state == "menu":
        draw_tiled_bg(screen, menu_bg_orig)
        if start_button.draw(screen) and next_state is None:
            next_state = "game"
            grid.saved_grid = None
            grid.saved_test_grid = None
            grid.saved_bombs = None
            grid.saved_occupied = None
            grid.saved_bomb_answers = None
        if tuto_button.draw(screen) and next_state is None:
            next_state = "tutorial"
        if quit_button.draw(screen):
            run = False

    elif state == "game":
        scroll = pygame.Surface(
            (screen.get_width(), max(screen.get_height(), int(1080 * current_scale)))
        )
        draw_tiled_bg(scroll, game_bg_orig)
        grid.draw_all(pygame, scroll, scroll_offset)

        adjusted_mouse = (
            pygame.mouse.get_pos()[0],
            pygame.mouse.get_pos()[1] + scroll_offset,
        )
        iesniegt_button.draw(scroll, adjusted_mouse)
        restartet_button.draw(scroll, adjusted_mouse)

        if grid.game_over:
            grid.restart_allowed = True
            if grid.win:
                won_surface = game_font2.render("Tu uzvarēji!", False, (0, 255, 0))
                scroll.blit(
                    won_surface, (int(800 * current_scale), int(535 * current_scale))
                )
            else:
                fail_surface = game_font2.render(
                    "Kļūda! - viss eksplodēja!", False, (255, 0, 0)
                )
                scroll.blit(
                    fail_surface, (int(800 * current_scale), int(535 * current_scale))
                )

        if game_back_button.draw(scroll, adjusted_mouse) and next_state is None:
            next_state = "menu"
            grid.save_game()

        screen.blit(scroll, (0, -scroll_offset))

        scrollbar_x = screen.get_width() - int(40 * current_scale)
        current_scrollbar = ScrollBar(
            scrollbar_x,
            0,
            screen.get_height(),
            int(120 * current_scale),
            (0, 0, 0),
            current_scale,
        )
        current_scrollbar.scroll_percent = scrollbar.scroll_percent
        current_scrollbar.thumb_y = scrollbar.y + scrollbar.scroll_percent * max(
            0, current_scrollbar.h - current_scrollbar.thumb_h
        )
        current_scrollbar.draw(screen)

    elif state == "tutorial":
        scroll = pygame.Surface(
            (screen.get_width(), max(screen.get_height(), int(950 * current_scale)))
        )
        # Stretch tutorial background to fit instead of tiling
        stretched_bg = pygame.transform.scale(
            tutorial_bg_orig, (scroll.get_width(), scroll.get_height())
        )
        scroll.blit(stretched_bg, (0, 0))
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
            " un ir ievadīti pareizie cipari zem abām bumbām.",
        ]

        for line in text:
            surface = font.render(line, True, (0, 0, 0))
            scroll.blit(surface, (int(20 * current_scale), y))
            y += int(35 * current_scale)

        adjusted_mouse_tuto = (
            pygame.mouse.get_pos()[0],
            pygame.mouse.get_pos()[1] + scroll_offset,
        )
        if back_button.draw(scroll, adjusted_mouse_tuto) and next_state is None:
            next_state = "menu"

        screen.blit(scroll, (0, -scroll_offset))

        scrollbar_x = screen.get_width() - int(40 * current_scale)
        tuto_scrollbar = ScrollBar(
            scrollbar_x,
            0,
            screen.get_height(),
            int(120 * current_scale),
            (0, 0, 0),
            current_scale,
        )
        tuto_scrollbar.scroll_percent = scrollbar.scroll_percent
        tuto_scrollbar.thumb_y = scrollbar.y + scrollbar.scroll_percent * max(
            0, tuto_scrollbar.h - tuto_scrollbar.thumb_h
        )
        tuto_scrollbar.draw(screen)

    if next_state is not None:
        state = next_state
        state_changed = True
        for btn in [
            start_button,
            quit_button,
            tuto_button,
            back_button,
            game_back_button,
            iesniegt_button,
            restartet_button,
        ]:
            btn.clicked = True
            btn.mouse_was_pressed = True

    pygame.display.flip()

pygame.quit()
