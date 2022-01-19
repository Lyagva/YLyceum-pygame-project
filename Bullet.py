# Класс пули. Пуля

# Импорт библиотек
import math
import random

import pygame as pg

import Explosion


class Bullet(pg.sprite.Sprite):
    def __init__(self, app, state, weapon, not_collide, to_pos):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.weapon = weapon
        self.not_collide = not_collide

        self.x, self.y = self.weapon.player.rect.center

        self.distance = self.weapon.distance
        self.damage = self.weapon.damage

        self.rect = pg.Rect(self.x,
                            self.y,
                            self.state.map.block_size[0] / 3,
                            self.state.map.block_size[1] / 3)

        self.image = pg.image.load("images/entities/Bullet.png")
        self.image = pg.transform.scale(self.image, self.rect.size)

        self.speed = self.weapon.speed / 10

        self.pos = (self.x, self.y)

        distance_x = to_pos[0] - self.x
        distance_y = to_pos[1] - self.y

        angle = math.atan2(distance_y, distance_x)
        if self.weapon.spread[0] != 0:
            angle += math.radians(random.randint(int(-self.weapon.spread[0] * 100),
                                            int(self.weapon.spread[0] * 100)) / 100)

        self.pos = (self.x + self.weapon.rect.width / 2 * math.cos(angle),
                    self.y + self.weapon.rect.height / 2 * math.sin(angle))
        self.vel = (self.speed * math.cos(angle), self.speed * math.sin(angle))

    def update(self):
        if self.distance <= 0:
            self.kill()

        self.movement()
        self.wall_collision()

    def render(self):
        self.app.screen.blit(self.image, self.rect)

    def movement(self):
        self.pos = (self.pos[0] + self.vel[0] * self.app.clock.get_time(),
                    self.pos[1] + self.vel[1] * self.app.clock.get_time())

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.distance -= ((self.vel[0] * self.app.clock.get_time()) ** 2 +
                          (self.vel[1] * self.app.clock.get_time()) ** 2) ** 0.5

    def wall_collision(self):
        map = self.state.map.return_map()

        for y in range(self.state.map.map_size[1]):
            for x in range(self.state.map.map_size[0]):
                other = map[y][x]

                if other:
                    if pg.sprite.collide_rect(self, other) and other.type not in ["lever", "prop", "lava"]:
                        if other.type in ["forcefield", "destroyableblock"]:
                            if self.weapon.bullet_type == "phys":
                                other.get_damage(self.damage)

                        if self.weapon.bullet_type == "exp":
                            self.state.explosions.add(Explosion.Explosion(self.app, self.state, self.pos, self.damage))
                        self.kill()

        # check damage mob
        if self.not_collide != "mob":
            for sprite in pg.sprite.spritecollide(self, self.state.mobs, False):
                if self.weapon.bullet_type == "phys":
                    sprite.get_damage(self.damage, self.pos)
                elif self.weapon.bullet_type == "exp":
                    self.state.explosions.add(Explosion.Explosion(self.app, self.state, self.pos, self.damage))
                self.kill()

        # check damage player
        if self.not_collide != "player":
            if pg.sprite.collide_rect(self, self.state.player):
                if self.weapon.bullet_type == "phys":
                    self.state.player.get_damage(self.damage)
                elif self.weapon.bullet_type == "exp":
                    self.state.explosions.add(Explosion.Explosion(self.app, self.state, self.pos, self.damage))
                self.kill()
