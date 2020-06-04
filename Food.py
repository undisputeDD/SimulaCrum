import pygame

class Food(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, screen):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()
        image = pygame.image.load("../data/icons/gem.png").convert_alpha()
        image = pygame.transform.scale(image, (60, 60))
        # self.image = pygame.Surface([width, height])
        self.image = image
        self.screen = screen
        self.rect = self.image.get_rect()

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))