# Это класс с базовой структурой блока. У него есть коллизия и текстура.

# Импорт библиотек
import pygame as pg

class Block:
    # Позиция идёт относительная, то есть это не координаты на экране, а координаты карты
    def __init__(self, app, map_arg, pos):
        self.app = app
        self.map = map_arg
        self.pos = pos

        self.current_offset = self.map.map_offset
        self.rect = pg.Rect((self.pos[0] * self.map.block_size[0] - self.map.map_offset[0],
                             self.pos[1] * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))


    def update(self):
        # Движение
        self.rect.update((self.pos[0] * self.map.block_size[0] - self.map.map_offset[0],
                             self.pos[1] * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))
        self.current_offset = self.map.map_offset



    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            pg.draw.rect(self.app.screen,
                         (0, 32 + ((255 - 32) / self.map.map_size[0] * self.pos[0]),
                          32 + ((255 - 32) / self.map.map_size[1] * self.pos[1])), # Тут просто градиентик
                         self.rect)