import pygame
from settings import screen_width, screen_height, map, tile_size, level_width, level_height
from world import World
from camera import Camera

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("img/background3.png").convert()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)


camera = Camera(screen_width, screen_height, level_width, level_height)

world = World(screen, map)


x_active = False
running = True
while running:
    keys = pygame.key.get_pressed()
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    world.run(camera)


    current_fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(current_fps)}", True, (0, 255, 0))
    screen.blit(fps_text, (10, 10))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
