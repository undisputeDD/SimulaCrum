import pygame
import random
import math


class Blop(pygame.sprite.Sprite):

    def __init__(self, screen, style, kind):

        # Call the parent class (Sprite) constructor
        super().__init__()
        image = pygame.image.load(f'../data/icons/blop/{style}.png').convert_alpha()
        image = pygame.transform.scale(image, (60, 60))
        # self.image = pygame.Surface([width, height])
        self.image = image
        self.screen = screen
        self.kind = kind
        self.x = 0
        self.energy = kind['survival']
        self.y = 0
        self.rect = self.image.get_rect()

    def move(self):
        x = y = -1
        while (x > 0) and (y > 0):
            step = self.kind['speed'].get()
            angle = random.randint(0, 360)
            cos = math.cos(math.radians(angle))
            sin = math.sin(math.radians(angle))
            x = self.x + step * cos
            y = self.y + step * sin
        self.screen.blit(self.image, (x + y))
        return x, y
        # self.draw(self.)

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))
