from settings import tile_size

class Camera:
    def __init__(self, width, height, level_width, level_height):
        self.width = width
        self.height = height

        self.level_width = level_width
        self.level_height = level_height

        self.x = 0
        self.y = 0

    def update(self, target):
        self.x = target.centerx - self.width // 2
        self.y = target.centery - self.height // 2

        # Kamera ne menjen a pálya bal/felső szélén túl
        self.x = max(tile_size, self.x)
        self.y = max(tile_size, self.y)

        # Kamera ne menjen a pálya jobb/alsó szélén túl
        self.x = min(self.x, self.level_width - self.width - tile_size)
        self.y = min(self.y, self.level_height - self.height - tile_size)

    def apply(self, rect):
        return rect.move(-self.x, -self.y)