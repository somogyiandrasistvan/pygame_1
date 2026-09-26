def load_level_map(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        level_map = [line.rstrip("\r\n") for line in file]
    return level_map

map = load_level_map("map/map.txt")

screen_width = 1200
screen_height = 700

tile_size = 64

level_width = len(map[0]) * tile_size
level_height = len(map) * tile_size





