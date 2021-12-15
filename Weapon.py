# Класс оружий. Тип пуль, урон, статы и т.д. тут.

# Импорт библиотек
import math

import pygame as pg

import Bullet


class Weapon(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, player):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.main_gameplay = main_gameplay
        self.player = player

        self.rect = pg.Rect(self.player.rect.center[0], self.player.rect.center[1], 50, 20)

        self.bullets_per_second = 50
        self.shoot_cd = [0, 1 / self.bullets_per_second] # Время между выстрелами. Слева действующие числа, справа число для сброса

        self.damage = 1
        self.spread = [0, 0.1, 0, 15, 1] # Разброс в градусах. 0 текущий, 1 дельта, 2 мин, 3 макс, 4 время до сброса
        self.speed = 10
        self.bullets_per_time = 1
        self.distance = 1000

    def update(self):
        self.rect.x, self.rect.y = self.player.rect.center

        self.shoot_cd[0] -= self.app.clock.get_time() / 1000
        self.spread_op()
        self.shoot()
        # print(self.spread[0])

    def render(self):
        pg.draw.rect(self.app.screen, (0, 0, 255), self.rect)

    def spread_op(self):
        if -self.shoot_cd[0] + self.shoot_cd[1] > self.spread[4]:
            self.spread[0] -= self.spread[1]

        if self.spread[0] < self.spread[2]:
            self.spread[0] = self.spread[2]

        if self.spread[0] > self.spread[3]:
            self.spread[0] = self.spread[3]

    def shoot(self):
        if pg.mouse.get_pressed(3)[0] and self.shoot_cd[0] <= 0:
            for _ in range(self.bullets_per_time):
                self.main_gameplay.bullets.add(Bullet.Bullet(self.app, self.main_gameplay, self))
                self.shoot_cd[0] = self.shoot_cd[1]
                self.spread[0] += self.spread[1]