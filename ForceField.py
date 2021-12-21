# Класс блока, через который не проходят пули

import pygame as pg


class ForceField(pg.sprite.Sprite):
    def __init__(self, app, map_arg, pos, image=None, health=100):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.map = map_arg
        self.x, self.y = pos
        self.type = "forcefield"

        self.rect = pg.Rect((self.x * self.map.block_size[0] - self.map.map_offset[0],
                             self.y * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))

        self.image = image
        if self.image:
            self.image = pg.image.load(self.image)
            self.image = pg.transform.scale(self.image, self.rect.size)

        self.health = health

    def update(self):
        if self.health != "inf" and self.health <= 0:
            for row in range(self.map.map_size[1]):
                for col in range(self.map.map_size[0]):
                    if self.map.map[row][col] == self:
                        self.map.map[row][col] = None

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             (100, 150, 255),
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

    def get_damage(self, damage):
        if self.health != "inf":
            self.health -= damage
