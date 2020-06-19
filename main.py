import pygame

# Flags and global data
menu_button_obj = []
simulation_button_obj = []
menu_mode = 1

# Array of species
organisms = []

class Button:
    def __init__(self, msg, x, y, w, h, ic, ac, startText, textSurf, textRect, action=None, image=None):
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
        self._image = image

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

    def get_image(self):
        return self._image

    def perform_action(self):
        self._action()


def decode_template(filename):
    with open(filename) as file:
        contents = file.read()
    data = {}
    catalogue = []
    chapters = contents.split('&')
    for line in chapters[0].split("\n"):
        splits = line.split('|')
        if len(splits) == 2:
            data[splits[0]] = splits[1]

    for kinds in chapters[1].split("@"):
        print(kinds)
        blop_kind = {}
        for line2 in kinds.split("\n"):
            splits = line2.split('|')
            if len(splits) == 2:
                blop_kind[splits[0]] = splits[1]
        if len(blop_kind) != 0:
            catalogue.append(blop_kind)
    return data, catalogue


def start_simulation_func():
    data, catalogue = decode_template('Fabula.crum')
    field = []
    for i in range(FIELD_SIZE):
        vert = []
        for j in range(FIELD_SIZE):
            vert.append(0)
        field.append(vert)

    print(data)
    print(catalogue)
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            print(str(field[i][j]) + ' ', end='')
        print()


def pause_simulation_func():
    pass


def end_simulation_func():
    global menu_mode
    menu_mode = 1


def start_func():
    print('! START IS CALLED !')
    global menu_mode
    menu_mode = 0


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


def create_simulation_button(msg, x, y, w, h, ic, ac, action):
    # Setting up button`s text properties

    file = ""
    if action == start_simulation_func:
        file = 'start.png'
    elif action == pause_simulation_func:
        file = 'pause.jpg'
    elif action == end_simulation_func:
        file = 'stop.png'
    else:
        print("!!! Error creating simulation buttons !!!")

    img = pygame.image.load('images/' + file)
    img_rect = pygame.Rect((x, y), (w, h))
    img_surf = pygame.Surface((w, h))
    img = pygame.transform.scale(img, (w, h))

    button = Button(msg, x, y, w, h, ic, ac, None, img_surf, img_rect, action, img)
    simulation_button_obj.append(button)


def draw_menu_condition():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for button in menu_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > mouse_pos[1] > button.get_y():
            pygame.draw.rect(screen, button.get_ac(), (button.get_x(), button.get_y(), button.get_w(), button.get_h()))
            if click[0] == 1 and button.get_action() is not None:
                button.perform_action()
        else:
            pygame.draw.rect(screen, button.get_ic(), (button.get_x(), button.get_y(), button.get_w(), button.get_h()))
        screen.blit(button.get_textSurf(), button.get_textRect())


def draw_simulation_condition():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for button in simulation_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > mouse_pos[1] > button.get_y():
            if click[0] == 1 and button.get_action() is not None:
                button.perform_action()
        screen.blit(button.get_image(), button.get_textRect())

    background_panel = pygame.Surface((FIELD_WIDTH, FIELD_HEIGHT))
    background_panel.fill(LIGHT_BLUE)
    background_panel_rect = pygame.Rect((0, 0), (FIELD_WIDTH, FIELD_HEIGHT))

    screen.blit(background_panel, background_panel_rect)


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

# Background setting
FIELD_WIDTH = WINDOW_HEIGHT
FIELD_HEIGHT = WINDOW_HEIGHT
img = pygame.image.load('images/background.png')
img_rect = pygame.Rect((0, 0), (FIELD_WIDTH, FIELD_HEIGHT))
img = pygame.transform.scale(img, (FIELD_WIDTH, FIELD_HEIGHT))

# Size of simulation field
FIELD_SIZE = 10

PANEL_WIDTH = WINDOW_WIDTH - FIELD_WIDTH
PANEL_HEIGHT = WINDOW_HEIGHT
panel = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT))
panel.fill(GREY)
panel_rect = pygame.Rect((FIELD_WIDTH, 0), (PANEL_WIDTH, PANEL_HEIGHT))

# Fps setting
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

# Adding menu buttons
create_button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
create_button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
create_button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)

# Adding simulation buttons
create_simulation_button('START', 720 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, start_simulation_func)
create_simulation_button('PAUSE', 720 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, pause_simulation_func)
create_simulation_button('END', 720 + 47.5 + 38 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, end_simulation_func)

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
        draw_menu_condition()
        simulation_button_obj = []
        create_simulation_button('START', 720 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, start_simulation_func)
        create_simulation_button('PAUSE', 720 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, pause_simulation_func)
        create_simulation_button('END', 720 + 47.5 + 38 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, end_simulation_func)
    else:
        draw_simulation_condition()
        menu_button_obj = []
        create_button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
        create_button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
        create_button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)

    # Updating
    pygame.display.update()  # Or pygame.display.flip()
