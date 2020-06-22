import pygame
from button import Button


# Program conditions
def start_simulation_func():
    global mode
    mode = 2
    # mode - 2[simulation working process]


def pause_simulation_func():
    global mode
    if mode == 2:
        mode = 3
        # mode - 3[simulation pause process]
    elif mode == 3:
        mode = 2
        # mode - 2[simulation working process]


def end_simulation_func():
    global mode
    mode = 1
    # mode - 1[menu mode]


def start_func():
    print('! START IS CALLED !')
    global mode
    mode = 0
    # mode - 0[simulation waiting process]


def settings_func():
    print('! SETTINGS IS CALLED !')
    # mode - 1[menu mode]


def quit_func():
    print('! QUIT IS CALLED !')
    pygame.quit()
    quit()


# Buttons functions
def create_menu_button(msg, x, y, w, h, ic, ac, action):
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
    if action == start_simulation_func or action is None:
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


# Drawing of different conditions
def draw_menu_condition():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Background elements
    global panel, panel_rect
    screen.blit(panel, panel_rect)
    global img, img_rect
    screen.blit(img, img_rect)

    # Buttons
    for button in menu_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > \
                mouse_pos[1] > button.get_y():
            pygame.draw.rect(screen, button.get_ac(), (button.get_x(), button.get_y(), button.get_w(), button.get_h()))
            if click[0] == 1 and button.get_action() is not None:
                button.perform_action()
        else:
            pygame.draw.rect(screen, button.get_ic(), (button.get_x(), button.get_y(), button.get_w(), button.get_h()))
        screen.blit(button.get_textSurf(), button.get_textRect())


def draw_simulation_condition():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Background elements
    global panel, panel_rect
    screen.blit(panel, panel_rect)
    global img, img_rect
    screen.blit(img, img_rect)

    # Buttons
    for button in simulation_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > \
                mouse_pos[1] > button.get_y():
            if click[0] == 1 and button.get_action() is not None:
                button.perform_action()
        screen.blit(button.get_image(), button.get_textRect())


def draw_simulation_working_condition():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Background elements
    global panel, panel_rect
    screen.blit(panel, panel_rect)
    global img, img_rect
    screen.blit(img, img_rect)

    # Buttons
    for button in simulation_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > \
                mouse_pos[1] > button.get_y():
            if click[0] == 1 and button.get_action() is not None:
                button.perform_action()
        screen.blit(button.get_image(), button.get_textRect())

    print('Work simulation')
    # pygame.time.wait(3000)


def draw_simulation_pause_condition():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Background elements
    global panel, panel_rect
    screen.blit(panel, panel_rect)
    global img, img_rect
    screen.blit(img, img_rect)

    # Buttons
    for button in simulation_button_obj:
        if button.get_x() + button.get_w() > mouse_pos[0] > button.get_x() and button.get_y() + button.get_h() > \
                mouse_pos[1] > button.get_y():
            if click[0] == 1 and button.get_action() is not None:
                button.perform_action()
        screen.blit(button.get_image(), button.get_textRect())

    print('Pause simulation')
    # pygame.time.wait(3000)


if __name__ == '__main__':
    # Flags and global data

    # Color setting
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (173, 216, 230)
    GREY = (58, 58, 60)
    BLUE_GREY = (112, 128, 144)

    # Initialisation of a program
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))

    # Window setting
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 720
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Background setting
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

    # Buttons
    menu_button_obj = []
    simulation_button_obj = []

    # Program mode
    mode = 1
    # mode - 0[simulation waiting process]
    # mode - 1[menu mode]
    # mode - 2[simulation working process]
    # mode - 3[simulation pause process]

    # Adding menu buttons
    create_menu_button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
    create_menu_button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
    create_menu_button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)

    # Adding simulation buttons
    create_simulation_button('START', 720 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, start_simulation_func)
    create_simulation_button('PAUSE', 720 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, pause_simulation_func)
    create_simulation_button('END', 720 + 47.5 + 38 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                             end_simulation_func)

    # Main loop
    while True:
        clock.tick(FPS)

        print(mode)

        # Event handler
        for event in pygame.event.get():
            pass

        # Drawing conditions
        if mode == 0:
            draw_simulation_condition()
            menu_button_obj = []
            create_menu_button('Start', 796, 478, 152, 30, LIGHT_BLUE, BLUE_GREY, start_func)
            create_menu_button('Settings', 796, 546, 152, 30, LIGHT_BLUE, BLUE_GREY, settings_func)
            create_menu_button('Quit', 796, 614, 152, 30, LIGHT_BLUE, BLUE_GREY, quit_func)
        elif mode == 1:
            draw_menu_condition()
            simulation_button_obj = []
            create_simulation_button('START', 720 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, start_simulation_func)
            create_simulation_button('PAUSE', 720 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                                     pause_simulation_func)
            create_simulation_button('END', 720 + 47.5 + 38 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                                     end_simulation_func)
        elif mode == 2:
            draw_simulation_working_condition()
            simulation_button_obj = []
            create_simulation_button('START', 720 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, None)
            create_simulation_button('PAUSE', 720 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                                     pause_simulation_func)
            create_simulation_button('END', 720 + 47.5 + 38 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                                     end_simulation_func)
        elif mode == 3:
            draw_simulation_pause_condition()
            simulation_button_obj = []
            create_simulation_button('START', 720 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY, start_simulation_func)
            create_simulation_button('PAUSE', 720 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                                     pause_simulation_func)
            create_simulation_button('END', 720 + 47.5 + 38 + 47.5 + 38 + 47.5, 546, 38, 38, LIGHT_BLUE, BLUE_GREY,
                                     end_simulation_func)

        # Updating
        pygame.display.update()  # Or pygame.display.flip()
