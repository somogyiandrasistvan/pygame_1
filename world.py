from random import random

import pygame
from settings import tile_size
from player import Player
from tiles.drops import Block
from tiles.tiles import Foreground


class World:
    def __init__(self, surface, map):
        self.display_surface = surface

        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
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
        self.update_grass_tiles()

    def run(self, camera,dt):
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()


        player = self.player.sprite
        camera.update(player.rect)

        for sprite in self.tiles.sprites():
            self.display_surface.blit(sprite.image,camera.apply(sprite.rect))

        for sprite in self.drops.sprites():
            self.display_surface.blit(sprite.image, camera.apply(sprite.rect))
        self.drops.update(dt)
        self.display_surface.blit(player.image,camera.apply(player.rect))




    def delete_tile(self, pos):
        for tile in self.tiles:
            if tile.x == pos[0] and tile.y == pos[1]:
                if tile.damage():
                    self.tiles.remove(tile)
                    self.update_grass_tiles(pos[0], pos[1])
                    self.drops.add(Block(tile_size // 2, pos[0], pos[1], tile.name, 1))







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


    def update_grass_tiles(self, target_x=None, target_y=None):
        # Összes blokk koordinátáinak kigyűjtése gyors kereséshez (O(1))
        occupied_tiles = {(t.x, t.y): t for t in self.tiles}

        def refresh_tile(t):
            if t and t.name in ("dirt", "dirt_2"):
                # Megnézzük, van-e blokk közvetlenül felette (y - tile_size)
                tile_above = occupied_tiles.get((t.x, t.y - tile_size))
                has_dirt_above = tile_above is not None #and tile_above.category == "block"
                if not has_dirt_above:
                    t.change_type("dirt_2")
                else:
                    t.change_type("dirt")

        # 1. eset: Target=Have
        if target_x is not None and target_y is not None:
            current_tile = next((t for t in self.tiles if t.x == target_x and t.y == target_y), None)
            below_tile = next((t for t in self.tiles if t.x == target_x and t.y == target_y + tile_size), None)
            refresh_tile(current_tile)
            refresh_tile(below_tile)


        # 2. eset: Target=None
        else:
            for tile in self.tiles:
                refresh_tile(tile)

    def get_player(self):
        return self.player.sprite


   #def block_drop(drop_chance=0.5, min_amount=1, max_amount=3):
   #    if random.random() < drop_chance:
   #        return random.randint(min_amount, max_amount)
   #    return 0