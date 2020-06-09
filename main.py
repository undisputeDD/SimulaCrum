import pygame


def start_func():
    print('! START IS CALLED !')


def settings_func():
    print('! SETTINGS IS CALLED !')


def quit_func():
    print('! QUIT IS CALLED !')


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse_pos[0] > x and y + h > mouse_pos[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    startText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf = startText.render(msg, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

# Window setting
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Color setting
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREY = (58, 58, 60)
BLUE_GREY = (112, 128, 144)

# Background settind
FIELD_WIDTH = WINDOW_HEIGHT
FIELD_HEIGHT = WINDOW_HEIGHT
img = pygame.image.load('images/background.png')
img_rect = pygame.Rect((0, 0), (FIELD_WIDTH, FIELD_HEIGHT))
img = pygame.transform.scale(img, (FIELD_WIDTH, FIELD_HEIGHT))

PANEL_WIDTH = WINDOW_WIDTH - FIELD_WIDTH
PANEL_HEIGHT = WINDOW_HEIGHT
panel = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT))
panel.fill(GREY)
panel_rect = pygame.Rect((FIELD_WIDTH, 0), (PANEL_WIDTH, PANEL_HEIGHT))

# Fps setting
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

# White test rectangle setting
white_rect = pygame.Surface((32, 32))
white_rect.fill(WHITE)
white_rect_rect = pygame.Rect((0, 0), (32, 32))

# Main loop
while True:
    clock.tick(FPS)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                white_rect_rect.move_ip(0, -20)
            elif event.key == pygame.K_s:
                white_rect_rect.move_ip(0, 20)
            elif event.key == pygame.K_a:
                white_rect_rect.move_ip(-20, 0)
            elif event.key == pygame.K_d:
                white_rect_rect.move_ip(20, 0)

    # Drawing
    screen.blit(img, img_rect)
    screen.blit(white_rect, white_rect_rect)
    screen.blit(panel, panel_rect)

    # Adding buttons
    button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
    button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
    button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)

    # Updating
    pygame.display.update()  # Or pygame.display.flip()
