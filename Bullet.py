# Класс пули. Пуля

# Импорт библиотек
import math
import random

import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, weapon):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.main_gameplay = main_gameplay
        self.weapon = weapon

        self.x, self.y = self.weapon.rect.right, self.weapon.rect.centery
        self.size = 10, 10
        self.pos = (self.x, self.y)
        self.distance = self.weapon.distance
        self.damage = self.weapon.damage

        self.rect = pg.Rect(self.x,
                            self.y,
                            self.size[0],
                            self.size[1])

        self.speed = self.weapon.speed / 10

        mouse_x, mouse_y = pg.mouse.get_pos()

        distance_x = mouse_x - self.x
        distance_y = mouse_y - self.y

        angle = math.atan2(distance_y, distance_x)
        if self.weapon.spread[0] != 0:
            angle += math.radians(random.randint(int(-self.weapon.spread[0] * 100),
                                            int(self.weapon.spread[0] * 100)) / 100)

        self.vel = (self.speed * math.cos(angle), self.speed * math.sin(angle))

    def update(self):
        if self.distance <= 0:
            self.kill()

        self.movement()
        self.wall_collision()

    def render(self):
        pg.draw.rect(self.app.screen, (255, 0, 0), self.rect)

    def movement(self):
        self.pos = (self.pos[0] + self.vel[0] * self.app.clock.get_time(),
                    self.pos[1] + self.vel[1] * self.app.clock.get_time())

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.distance -= ((self.vel[0] * self.app.clock.get_time()) ** 2 +
                          (self.vel[1] * self.app.clock.get_time()) ** 2) ** 0.5

    def wall_collision(self):
        map = self.main_gameplay.map.return_map()

        for y in range(self.main_gameplay.map.map_size[1]):
            for x in range(self.main_gameplay.map.map_size[0]):
                other = map[y][x]

                if other:
                    if pg.sprite.collide_rect(self, other):
                        if other.type in ["forcefield", "destroyableblock"]:
                            other.get_damage(self.damage)

                        self.kill()
