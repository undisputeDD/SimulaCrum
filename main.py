import pygame

# Flags and global data
menu_button_obj = []
menu_mode = 1


class Button:
    def __init__(self, msg, x, y, w, h, ic, ac, startText, textSurf, textRect, action=None):
        self._msg = msg
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._ic = ic
        self._ac = ac
        self._startText = startText
        self._textSurf = textSurf
        self._textRect = textRect
        self._action = action

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_w(self):
        return self._w

    def get_h(self):
        return self._h

    def get_ic(self):
        return self._ic

    def get_ac(self):
        return self._ac

    def get_startText(self):
        return self._startText

    def get_textSurf(self):
        return self._textSurf

    def get_textRect(self):
        return self._textRect

    def get_action(self):
        return self._action

    def perform_action(self):
        self._action()


def start_func():
    print('! START IS CALLED !')
    # global menu_mode
    # menu_mode = 1
    pygame.time.wait(5000)


def settings_func():
    print('! SETTINGS IS CALLED !')


def quit_func():
    print('! QUIT IS CALLED !')
    pygame.quit()
    quit()


def create_button(msg, x, y, w, h, ic, ac, action):
    # Setting up button`s text properties
    startText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf = startText.render(msg, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ((x + (w / 2)), (y + (h / 2)))

    button = Button(msg, x, y, w, h, ic, ac, startText, textSurf, textRect, action)
    menu_button_obj.append(button)


def draw_buttons():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for button in menu_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > mouse_pos[1] > button.get_y():
            pygame.draw.rect(screen, button.get_ac(), (button.get_x(), button.get_y(), button.get_w(), button.get_h()))
            if click[0] == 1 and button.get_action() != None:
                if button.get_action() == start_func:
                    global menu_mode
                    menu_mode = 0
                    for check_button in menu_button_obj:
                        #check_button.get_textSurf().fill(GREY) <- Maybe no need
                        pygame.draw.rect(screen, GREY, (check_button.get_x(), check_button.get_y(), check_button.get_w(), check_button.get_h()))
                    pygame.display.update()  # To see if buttons are gone
                button.perform_action()
        else:
            pygame.draw.rect(screen, button.get_ic(), (button.get_x(), button.get_y(), button.get_w(), button.get_h()))
        screen.blit(button.get_textSurf(), button.get_textRect())


# Initialisation of a program
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

# Adding buttons
create_button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
create_button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
create_button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)

# White test rectangle setting
white_rect = pygame.Surface((32, 32))
white_rect.fill(WHITE)
white_rect_rect = pygame.Rect((0, 0), (32, 32))

# Main loop
while True:
    clock.tick(FPS)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
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

    # Drawing buttons
    if menu_mode == 1:
        draw_buttons()
    else:
        menu_mode = 1  # Hard code to bring buttons back
        menu_button_obj = []
        create_button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
        create_button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
        create_button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)

    # Updating
    pygame.display.update()  # Or pygame.display.flip()
