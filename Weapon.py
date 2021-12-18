# Класс оружий. Тип пуль, урон, статы и т.д. тут.

# Импорт библиотек
import math

import pygame as pg

import Bullet


class Weapon(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, player,
                 bullets_per_second = 50, damage = 5,
                 speed = 10, bullets_per_time = 1,
                 distance = 1000, spread = [0, 0.2, 0, 15, 1],
                 ammo = [30, 30, 100, 100], reload_time = 1):

        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.main_gameplay = main_gameplay
        self.player = player

        self.selected = False
        self.rect = None

        self.bullets_per_second = bullets_per_second
        self.shoot_cd = [0, 1 / self.bullets_per_second] # Время между выстрелами. Слева действующие числа, справа число для сброса

        self.damage = damage
        self.spread = spread # Разброс в градусах. 0 текущий, 1 дельта, 2 мин, 3 макс, 4 время до сброса
        self.speed = speed
        self.bullets_per_time = bullets_per_time
        self.distance = distance

        self.ammo = ammo # 0 в обойме, 1 макс в обойме, 2 в запасе, 3 макс в запасе
        self.reloading = False
        self.reload_time = [0, reload_time] # 0 текущее, 1 макс

    def update(self):
        if self.rect is None:
            self.rect = pg.Rect(self.player.rect.center[0], self.player.rect.center[1], 50, 20)

        self.rect.x, self.rect.y = self.player.rect.center

        self.shoot_cd[0] -= self.app.clock.get_time() / 1000
        self.spread_op()
        if self.selected:
            self.reload()

            if self.reloading:
                self.reload_time[0] -= self.app.clock.get_time() / 1000

            else:
                self.shoot()
                self.reload_time[0] = self.reload_time[1]
        else:
            self.reloading = False

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
        if pg.mouse.get_pressed(3)[0] and self.shoot_cd[0] <= 0 and self.ammo[0] > 0:
            self.ammo[0] -= 1
            for _ in range(self.bullets_per_time):
                self.main_gameplay.bullets.add(Bullet.Bullet(self.app, self.main_gameplay, self))

                self.shoot_cd[0] = self.shoot_cd[1]
                self.spread[0] += self.spread[1]

    def reload(self):
        if pg.key.get_pressed()[pg.K_r] and \
                self.ammo[0] != self.ammo[1] and \
                self.reload_time[0] >= 0 and \
                not self.reloading:

            self.reloading = True

        if self.reloading and self.reload_time[0] <= 0:
            picked_ammo = min(self.ammo[1] - self.ammo[0], self.ammo[2])
            self.ammo[2] -= picked_ammo
            self.ammo[0] += picked_ammo
            self.reloading = False