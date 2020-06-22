import random
import pygame
import Blop
import Food

width = height = 800
amount_food = 50
amount_creatures = 50


def decode_template(filename):
    with open(filename) as file:
        contents = file.read()
    data = {}
    catalogue = {}
    chapters = contents.split('&')
    for line in chapters[0].strip().split("\n"):
        splits = line.strip().split('|')
        data[splits[0]] = splits[1]

    for kind in chapters[1].split("@"):
        blop_kind = {}
        for line2 in kind.strip().split("\n"):
            splits = line2.strip().split('|')
            blop_kind[splits[0]] = splits[1]
        catalogue[blop_kind['name']] = blop_kind
    return data, catalogue


class Engine:

    def __init__(self, sim_data, blop_catalogue):
        pygame.init()
        self.sim_data = sim_data
        self.catalogue = blop_catalogue
        self.food_list = []
        self.food_coords = []
        self.blop_list = []
        self.ticks_max = sim_data['speed']
        self.style = sim_data['design']
        self.screen = pygame.display.set_mode((width, height))
        self.ticks = 0

    def tick(self):
        if self.ticks >= self.ticks_max:
            self.clear_screen()

        for blop in self.blop_list:
            x, y = blop.move()
            new_foods = []
            for food in self.food_list:
                f_x, f_y = food.x, food.y
                if (x - 10 <= f_x <= x + 10) and (y - 10 <= f_y <= y + 10):
                    print("Eaten!")
                    blop.energy += 1
                else:
                    new_foods.append(food)
            self.food_list = new_foods
            # if (x, y) in

        self.ticks += 1

    def generate_food(self):
        for i in range(amount_food):
            food = Food.Food(self.screen, self.sim_data['design'])
            self.food_list.append(food)
            x = 20 + round(random.random() * width)
            y = 20 + round(random.random() * height)
            self.food_coords.append((x, y))
            food.draw(x, y)

    def fill_board(self):
        style = self.sim_data['design'].get()

        background_image = pygame.image.load(f'./data/icons/backgrounds/{style}.png').convert()
        background_image = pygame.transform.scale(background_image, (width, height))
        self.screen.blit(background_image, [0, 0])

        for key, kind in self.catalogue.items():
            for _ in range(int(amount_creatures * kind['share'])):
                blop = Blop.Blop(self.screen, style, kind)
                self.blop_list.append(blop)

        pygame.display.init()
        pygame.display.update()

    def clear_screen(self):
        background_image = pygame.image.load(f'./data/icons/backgrounds/{self.style}.png').convert()
        background_image = pygame.transform.scale(background_image, (width, height))
        self.screen.blit(background_image, [0, 0])
        self.generate_food()
        self.review_blops()

    def review_blops(self):
        new_blop_list = []
        for blop in self.blop_list:
            if blop.energy < blop.kind['survive']:
                print("Died!")
            else:
                new_blop_list.append(blop)
                if blop.energy >= blop.kind['replica']:
                    kind = None # треба згенерувати по мутаціях, визначити, хто. Мутації це словник, може бути пустий
                    newbie = Blop.Blop(self.screen, self.style, kind)
                    new_blop_list.append(newbie)

        pass


sim_data, blop_catalogue = decode_template("./data/scenarios/Fabula.crum")
engine = Engine(sim_data, blop_catalogue)
