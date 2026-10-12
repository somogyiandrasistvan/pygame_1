import pygame


class Inventory:
    def __init__(self):
        self.size = 5
        self.slots = [{"item": None, "count": 0, "category": None} for _ in range(self.size)]
        self.selected_slot = 0
#----------AI--------
        self.slot_size = 40
        self.padding = 10
        self.font = pygame.font.Font(None, 24)
# --------------------

    def add_item(self, item, category):
        for slot in self.slots:
            if slot["item"] == item:
                slot["count"] += 1
                return True
        for slot in self.slots:
            if slot["item"] is None:
                slot["item"] = item
                slot["count"] = 1
                slot["category"] = category
                return True


        return False

    def remove_item(self, item):
        for slot in self.slots:
            if slot["item"] == item:
                slot["count"] -= 1
                if slot["count"] <= 0:
                    slot["item"] = None
                    slot["count"] = 0
                    slot["category"] = None
                return True
        return False

    def get_selected_item(self):
        return self.slots[self.selected_slot]["item"]

    def get_selected_item_category(self):
        return self.slots[self.selected_slot]["category"]


    def draw(self, surface):
        total_width = self.size * (self.slot_size + self.padding) - self.padding
        start_x = (surface.get_width() - total_width) // 2
        start_y = surface.get_height() - self.slot_size - 20

        for i, slot in enumerate(self.slots):
            x = start_x + i * (self.slot_size + self.padding)
            y = start_y

            rect = pygame.Rect(x, y, self.slot_size, self.slot_size)

            # Háttér rajzolása
            pygame.draw.rect(surface, (50, 50, 50), rect)

            # Keret: ha ez a kiválasztott slot, sárga, amúgy fehér
            color = (
                (255, 215, 0) if i == self.selected_slot else (200, 200, 200)
            )
            pygame.draw.rect(surface, color, rect, 3)

            # Tárgy név / ikon kirajzolása
            if slot["item"] is not None:
                # 1. Kép betöltése
                name = slot["item"]
                category = slot["category"]
                picture = pygame.image.load(f"img/{category}s/{name}.png").convert_alpha()

                picture = pygame.transform.scale(picture, (20, 20))

                # 2. Kép kirajzolása közvetlenül
                surface.blit(picture, (x + 10, y + 10))

                # 3. Darabszám kiírása a jobb alsó sarokba
                count_surface = self.font.render(
                    str(slot["count"]), True, (255, 255, 0)
                )
                surface.blit(count_surface, (x + 22, y + 22))
