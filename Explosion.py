# Взрыв

import pygame as pg


class Explosion(pg.sprite.Sprite):
    def __init__(self, app, state, pos, damage):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.pos = pos
        self.damage = damage

        self.radius = [0, 1000, 100]  # 0 текущий, 1 дельта, 2 макс

        self.rect = pg.Rect(self.pos[0] - self.radius[2] / 2, self.pos[1] - self.radius[2] / 2, self.radius[2], self.radius[2])
        self.rect_0_25 = pg.Rect(self.rect.x + (self.rect.width * 0.25) / 2 * 3, self.rect.y + (self.rect.height * 0.25) / 2 * 3, self.rect.width * 0.25, self.rect.height * 0.25)
        self.rect_0_50 = pg.Rect(self.rect.x + (self.rect.width * 0.5) / 2, self.rect.y + (self.rect.height * 0.5) / 2, self.rect.width * 0.5, self.rect.height * 0.5)

        # Map collide & dmg
        _ = [self.check_collide(obj) for line in self.state.map.return_map() for obj in line if obj is not None and obj.type in ["destroyableblock", "forcefield"]]

        # Player collide & dmg
        self.check_collide(self.state.player)

        # mobs collide & dmg
        _ = [self.check_collide(other, pos=self.pos) for other in self.state.mobs]

    def check_collide(self, other, pos=None):
        if self.rect_0_25.colliderect(other.rect):  # 0.25 размера - дамаг полный
            other.get_damage(self.damage) if pos is None else other.get_damage(self.damage, pos)
        elif self.rect_0_50.colliderect(other.rect):  # 0.5 размера - дамаг * 0.5
            other.get_damage(round(self.damage * 0.5)) if pos is None else other.get_damage(round(self.damage * 0.5), pos)
        elif self.rect.colliderect(other.rect):  # весь размер - дамаг * 0.25
            other.get_damage(round(self.damage * 0.25)) if pos is None else other.get_damage(round(self.damage * 0.25), pos)

    def render(self):
        pg.draw.circle(self.app.screen, (192, 57, 43), self.pos, self.radius[0])
        pg.draw.circle(self.app.screen, (230, 126, 34), self.pos, self.radius[0] // 2)
        pg.draw.circle(self.app.screen, (241, 196, 15), self.pos, self.radius[0] // 4)

    def update(self):
        self.radius[0] += self.radius[1] * self.app.clock.get_time() / 1000
        if self.radius[0] >= self.radius[2]:
            self.kill()
