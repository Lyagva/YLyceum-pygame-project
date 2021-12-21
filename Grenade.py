# Граната

# Импорт библиотек
import math
import random

import pygame as pg

import Explosion


class Grenade(pg.sprite.Sprite):
    def __init__(self, app, state):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state

        self.x, self.y = self.state.player.rect.center
        self.size = 20, 20
        self.pos = (self.x, self.y)

        self.rect = pg.Rect(self.x,
                            self.y,
                            self.size[0],
                            self.size[1])

        self.force = 10
        self.damage = 100
        self.gravity = 50
        self.friction = 1
        self.bounce_reduction = 0.3

        mouse_x, mouse_y = pg.mouse.get_pos()

        distance_x = mouse_x - self.x
        distance_y = mouse_y - self.y

        angle = math.atan2(distance_y, distance_x)

        self.vel = (self.force * math.cos(angle), self.force * math.sin(angle))

        self.time = 1

    def update(self):
        self.time -= self.app.clock.get_time() / 1000
        if self.time <= 0:
            self.state.explosions.add(Explosion.Explosion(self.app, self.state, self.rect.center, self.damage))
            self.kill()

        self.movement()

    def render(self):
        pg.draw.rect(self.app.screen, (39, 174, 96), self.rect)

    def movement(self):
        dt = self.app.clock.get_time() / 1000

        # Gravity
        self.vel = (self.vel[0], self.vel[1] + self.gravity * dt)

        # Horizontal coll
        self.rect.x += self.vel[0]
        self.wall_collision(self.vel[0], 0)

        # Vertical coll
        self.rect.y += self.vel[1]
        self.wall_collision(0, self.vel[1])

    def wall_collision(self, speed_x, speed_y):
        map = self.state.map.return_map()

        for y in range(self.state.map.map_size[1]):
            for x in range(self.state.map.map_size[0]):
                other = map[y][x]
                if other and pg.sprite.collide_rect(self, other):
                    # Right
                    if speed_x > 0:
                        self.rect.right = other.rect.left
                        self.vel = (-self.vel[0] * self.bounce_reduction, self.vel[1])

                    # Left
                    if speed_x < 0:
                        self.rect.left = other.rect.right
                        self.vel = (-self.vel[0] * self.bounce_reduction, self.vel[1])

                    # Up
                    if speed_y < 0:
                        self.rect.top = other.rect.bottom
                        self.vel = (self.vel[0], 0)

                    # Down
                    if speed_y > 0:
                        self.rect.bottom = other.rect.top
                        self.on_ground = True
                        if self.vel[0] >= 0:
                            self.vel = (self.vel[0] - self.friction, 0)
                        if self.vel[0] < 0:
                            self.vel = (self.vel[0] + self.friction, 0)

                        if other.type == "jumppad":
                            self.vel = (self.vel[0], self.vel[1] - other.force)
                    else:
                        self.on_ground = False