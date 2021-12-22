import pygame as pg


class Mob(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, pos):
        pg.sprite.Sprite.__init__(self)

        self.app = app
        self.main_gameplay = main_gameplay

        self.x, self.y = pos
        self.rect = pg.Rect(0, 0, 0, 0)
        self.type = 'mob'

        self.health = [100, 100]  # 0 текущее хп, 1 макс хп

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x,
                                self.y,
                                self.main_gameplay.map.block_size[0] * 0.8,
                                self.main_gameplay.map.block_size[1] * 1.6)

    def render(self):
        pg.draw.rect(self.app.screen, (255, 255, 255), self.rect)

    def get_damage(self, dmg):
        self.health[0] -= dmg

