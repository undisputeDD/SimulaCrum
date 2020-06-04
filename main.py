import pygame
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

    mouse_pos = pygame.mouse.get_pos()

    if 796 + 152 > mouse_pos[0] > 796 and 478 + 30 > mouse_pos[1] > 478:
        pygame.draw.rect(screen, BLUE_GREY, (796, 478, 152, 30))
    else:
        pygame.draw.rect(screen, LIGHT_BLUE, (796, 478, 152, 30))

    if 796 + 152 > mouse_pos[0] > 796 and 546 + 30 > mouse_pos[1] > 546:
        pygame.draw.rect(screen, BLUE_GREY, (796, 546, 152, 30))
    else:
        pygame.draw.rect(screen, LIGHT_BLUE, (796, 546, 152, 30))

    if 796 + 152 > mouse_pos[0] > 796 and 614 + 30 > mouse_pos[1] > 614:
        pygame.draw.rect(screen, BLUE_GREY, (796, 614, 152, 30))
    else:
        pygame.draw.rect(screen, LIGHT_BLUE, (796, 614, 152, 30))

    # Updating
    pygame.display.update()  # Or pygame.display.flip()
