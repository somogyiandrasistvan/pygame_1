import pygame
from settings import screen_width, screen_height, map, tile_size, level_width, level_height
from world import World
from camera import Camera

import math


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("img/background3.png").convert()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)


camera = Camera(screen_width, screen_height, level_width, level_height)

world = World(screen, map)

def mouse_pos():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_x = mouse_x + camera.x
    world_y = mouse_y + camera.y
    grid_x = world_x // 64
    grid_y = world_y // 64
    x = grid_x * 64
    y = grid_y * 64
    return (x, y)

def is_in_build_zone(x, y):
    valid_x = 0 <= x < (level_width / 2)
    valid_y = (level_height / 2) <= y < level_height
    in_default_frame = valid_x and valid_y

    grid_x = int(x // 64)
    grid_y = int(y // 64)

    special_tile = False
    if 0 <= grid_y < len(map) and 0 <= grid_x < len(map[grid_y]):
        if map[grid_y][grid_x] == "-":
            special_tile = True

    return in_default_frame or special_tile


def is_in_reach(target_x, target_y, player_rect, max_blocks=2):
    player_grid_x = player_rect.centerx // 64
    player_grid_y = player_rect.centery // 64

    target_grid_x = target_x // 64
    target_grid_y = target_y // 64

    # Euklideszi távolság
    distance = math.hypot(target_grid_x - player_grid_x, target_grid_y - player_grid_y)

    return distance <= (max_blocks + 0.5)

x_active = False
running = True
while running:
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = mouse_pos()
            if is_in_build_zone(pos[0], pos[1]) and is_in_reach(pos[0], pos[1], world.get_player().rect, max_blocks=2):
                if event.button == 3:
                    selected_item = world.get_player().get_inventory().get_selected_item
                    if selected_item is not None:
                        world.add_tile(pos, selected_item)
                elif event.button == 1:
                    world.delete_tile(pos)


    world.run(camera, dt)


    world.get_player().get_inventory().draw(screen)

    current_fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(current_fps)}", True, (0, 255, 0))
    screen.blit(fps_text, (10, 10))
    pygame.display.update()


pygame.quit()
