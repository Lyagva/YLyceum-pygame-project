# Это класс с базовой структурой блока. У него есть коллизия и текстура.

# Импорт библиотек
import pygame as pg


class Block(pg.sprite.Sprite):
    # Позиция идёт относительная, то есть это не координаты на экране, а координаты карты
    def __init__(self, app, map_arg, pos, image=None):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.map = map_arg
        self.x, self.y = pos
        self.type = "block"

        self.rect = pg.Rect((self.x * self.map.block_size[0] - self.map.map_offset[0],
                             self.y * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))

        self.image = image
        if self.image:
            print(self.image)
            self.image = pg.image.load(self.image)
            self.image = pg.transform.scale(self.image, self.rect.size)

    def update(self):
        pass

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             (0, 32 + ((255 - 32) / self.map.map_size[0] * self.x),
                              32 + ((255 - 32) / self.map.map_size[1] * self.y)),  # Тут просто градиентик
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]
