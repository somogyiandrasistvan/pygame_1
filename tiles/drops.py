import math

import pygame


class Drop(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.x = x + 16
        self.y = y + 24
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.ido = 0

    def update(self, dt):
        self.ido += dt
        self.rect.centery = self.y + math.sin(self.ido * 3) * 4




class Block(Drop):
    def __init__(self, size, x, y, name, db):
        super().__init__(size, x, y)
        self.size = size
        self.name = name
        self.db = db
        loaded_image = pygame.image.load(f"img/drops/{name}_block.png").convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (size, size))


class Seed(Drop):
    def __init__(self, size, x, y, name):
        super().__init__(size, x, y)
        self.size = size
        self.name = name
        loaded_image = pygame.image.load(f"img/drops/{name}_seed.png").convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (size, size))