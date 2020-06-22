import pygame


class Food(pygame.sprite.Sprite):
    """
    This class represents the food.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, screen, style):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()
        image = pygame.image.load(f'../data/icons/food/{style}.png').convert_alpha()
        image = pygame.transform.scale(image, (60, 60))
        # self.image = pygame.Surface([width, height])
        self.image = image
        self.screen = screen
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect()

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))
        self.x = x
        self.y = y
