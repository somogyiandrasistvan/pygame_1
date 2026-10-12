import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = 5
        self.x = x
        self.y = y

    def damage(self):
        self.hp -= 1
        return self.hp <= 0




class Foreground(Tile):
    def __init__(self, size, x, y, name):
        super().__init__(size, x, y)
        self.size = size
        self.name = name
        loaded_image = pygame.image.load(f"img/tiles/foreground/{name}.png").convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (size, size))

    def change_type(self, new_type):
        loaded_image = pygame.image.load(f"img/tiles/foreground/{new_type}.png").convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (self.size, self.size))



class Background(Tile):
    def __init__(self, size, x, y, name):
        super().__init__(size, x, y)
        self.size = size

        loaded_image = pygame.image.load(f"img/tiles/foreground/{name}.png").convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (size, size))

