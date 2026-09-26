import pygame
from settings import tile_size
from player import Player
from tiles.tiles import Foreground


class World:
    def __init__(self, surface, map):
        self.display_surface = surface

        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()

        self.setup_world(map)


    def setup_world(self, map):
        for row_i, row in enumerate(map):
            for col_i, cell in enumerate(row):
                x = col_i * tile_size
                y = row_i * tile_size
                if cell == 'P':
                    self.player.add(Player((x, y)))
                if cell == '0':
                    self.tiles.add(Foreground(tile_size, x, y, "0"))
                if cell == '1':
                    self.tiles.add(Foreground(tile_size, x, y, "dirt"))
                if cell == '2':
                    self.tiles.add(Foreground(tile_size, x, y, "rock"))
                if cell == '3':
                    self.tiles.add(Foreground(tile_size, x, y, "lava"))

    def run(self, camera):
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()


        player = self.player.sprite
        camera.update(player.rect)

        for sprite in self.tiles.sprites():
            self.display_surface.blit(sprite.image,camera.apply(sprite.rect))
        self.display_surface.blit(player.image,camera.apply(player.rect))


    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

