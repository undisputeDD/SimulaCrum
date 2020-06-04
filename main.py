import pygame
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))


WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FIELD_WIDTH = WINDOW_HEIGHT
FIELD_HEIGHT = WINDOW_HEIGHT

img = pygame.image.load('images/background.png')
img_rect = pygame.Rect((0, 0), (FIELD_WIDTH, FIELD_HEIGHT))
img = pygame.transform.scale(img, (FIELD_WIDTH, FIELD_HEIGHT))

clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

white_rect = pygame.Surface((32, 32))
white_rect.fill(WHITE)
white_rect_rect = pygame.Rect((0, 0), (32, 32))

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                white_rect_rect.move_ip(0, -5)
            elif event.key == pygame.K_s:
                white_rect_rect.move_ip(0, 5)
            elif event.key == pygame.K_a:
                white_rect_rect.move_ip(-5, 0)
            elif event.key == pygame.K_d:
                white_rect_rect.move_ip(5, 0)

    screen.blit(img, img_rect)
    screen.blit(white_rect, white_rect_rect)
    pygame.display.update()  # Or pygame.display.flip()
