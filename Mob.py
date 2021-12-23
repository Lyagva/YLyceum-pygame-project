import math
import pygame as pg

import Weapon
from Functions import *


class Mob(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, pos):
        pg.sprite.Sprite.__init__(self)

        self.app = app
        self.main_gameplay = main_gameplay

        self.image = pg.Surface(
            (round(self.main_gameplay.map.block_size[0] * 0.8), round(self.main_gameplay.map.block_size[1] * 1.6)))
        self.image.fill(pg.Color('green'))

        self.x, self.y = pos
        self.rect = pg.Rect(0, 0, 0, 0)
        self.type = 'mob'

        self.health = [100, 100]  # 0 текущее хп, 1 макс хп

        self.weapons = [
            Weapon.Weapon(self.app, self.main_gameplay, self, ammo=[500, 500, 20000, 20000], bullet_type="exp")]
        self.selected_weapon = 0

        self.gravity = 10
        self.speed = (100, 20)
        self.vel = (0, 0)  # x, y
        self.on_ground = False

        self.visible = 600  # расстояние видимости

        # Raycasting
        self.lines = [
            # to player
            [[self.rect.center, self.main_gameplay.player.rect.center], []],

            # to right
            [[(self.rect.topright[0], self.rect.topright[1] + 5), (self.rect.topright[0] + self.visible, self.rect.topright[1] + 5)], []],
            [[(self.rect.right, self.rect.centery), (self.rect.right + self.visible, self.rect.centery)], []],
            [[(self.rect.bottomright[0], self.rect.bottomright[1] - 5), (self.rect.bottomright[0] + self.visible, self.rect.bottomright[1] - 5)], []],

            # to left
            [[(self.rect.topleft[0], self.rect.topleft[1] + 5), (self.rect.topleft[0] - self.visible, self.rect.topleft[1] + 5)], []],
            [[(self.rect.left, self.rect.centery), (self.rect.left - self.visible, self.rect.centery)], []],
            [[(self.rect.bottomleft[0], self.rect.bottomleft[1] - 5), (self.rect.bottomleft[0] - self.visible, self.rect.bottomleft[1] - 5)], []],


        ]

        self.max_time_jump = self.app.FPS / 5  # 1/5 секунда
        self.time_of_jump = 0
        self.go_to_left, self.go_to_right, self.go_jump = False, False, False

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x, self.y,
                                self.main_gameplay.map.block_size[0] * 0.8,
                                self.main_gameplay.map.block_size[1] * 1.6)

        # update visible
        if self.lines[0][1] or get_hypotenuse(self.lines[0][0][0][0],
                                              self.lines[0][0][1][0],
                                              self.lines[0][0][0][1],
                                              self.lines[0][0][1][1]) > self.visible:
            # не видит
            self.image.fill(pg.Color('green'))
        else:
            self.image.fill(pg.Color('red'))

        # update commands
        self.go_jump = True

        # update moves
        self.movement()

        # update Raycasting
        self.update_raycast()

    def update_raycast(self):
        easy_map = [obg for lst in self.main_gameplay.map.map for obg in lst if obg is not None]
        self.lines = [
            [[self.rect.center, self.main_gameplay.player.rect.center], lineRectIntersectionPoints([self.rect.center, self.main_gameplay.player.rect.center], easy_map)],

            [[(self.rect.topright[0], self.rect.topright[1] + 5), (self.rect.topright[0] + self.visible, self.rect.topright[1] + 5)], lineRectIntersectionPoints([(self.rect.topright[0], self.rect.topright[1] + 5), (self.rect.topright[0] + self.visible, self.rect.topright[1] + 5)], easy_map)],
            [[(self.rect.right, self.rect.centery), (self.rect.right + self.visible, self.rect.centery)], lineRectIntersectionPoints([(self.rect.right, self.rect.centery), (self.rect.right + self.visible, self.rect.centery)], easy_map)],
            [[(self.rect.bottomright[0], self.rect.bottomright[1] - 5), (self.rect.bottomright[0] + self.visible, self.rect.bottomright[1] - 5)], lineRectIntersectionPoints([(self.rect.bottomright[0], self.rect.bottomright[1] - 5), (self.rect.bottomright[0] + self.visible, self.rect.bottomright[1] - 5)], easy_map)],

            [[(self.rect.topleft[0], self.rect.topleft[1] + 5), (self.rect.topleft[0] - self.visible, self.rect.topleft[1] + 5)], lineRectIntersectionPoints([(self.rect.topleft[0], self.rect.topleft[1] + 5), (self.rect.topleft[0] - self.visible, self.rect.topleft[1] + 5)], easy_map)],
            [[(self.rect.left, self.rect.centery), (self.rect.left - self.visible, self.rect.centery)], lineRectIntersectionPoints([(self.rect.left, self.rect.centery), (self.rect.left - self.visible, self.rect.centery)], easy_map)],
            [[(self.rect.bottomleft[0], self.rect.bottomleft[1] - 5), (self.rect.bottomleft[0] - self.visible, self.rect.bottomleft[1] - 5)], lineRectIntersectionPoints([(self.rect.bottomleft[0], self.rect.bottomleft[1] - 5), (self.rect.bottomleft[0] - self.visible, self.rect.bottomleft[1] - 5)], easy_map)],

        ]

    def movement(self):
        dt = self.app.clock.get_time() / 1000

        self.vel = (0, self.vel[1])

        # Right
        if self.go_to_right:
            self.vel = (self.vel[0] + self.speed[0] * dt, self.vel[1])

        # Left
        if self.go_to_left:
            self.vel = (self.vel[0] - self.speed[0] * dt, self.vel[1])

        # Jump
        if self.go_jump and self.time_of_jump < self.max_time_jump:
            self.on_ground = False
            self.vel = (self.vel[0], self.vel[1] - self.speed[1] * dt)

        #  GRAVITI
        self.vel = (self.vel[0], self.vel[1] + self.gravity * dt)

        if not self.on_ground:
            self.time_of_jump += 1
        else:
            self.time_of_jump = 0

        # Horizontal coll
        self.rect.x += self.vel[0]
        self.wall_collision(self.vel[0], 0)

        # Vertical coll
        self.rect.y += self.vel[1]
        self.wall_collision(0, self.vel[1])

    def render(self):
        self.app.screen.blit(self.image, (self.rect.x, self.rect.y))

        pg.draw.circle(self.app.screen, pg.Color('red'), self.rect.center, self.visible, 4)

        # raycast
        for val in self.lines:
            pg.draw.line(self.app.screen, pg.Color('white'), val[0][0], val[0][1], 1)
            for point in val[1]:
                pg.draw.circle(self.app.screen, pg.Color('white'), point, 4)

    def get_damage(self, dmg):
        self.health[0] -= dmg

    def wall_collision(self, speed_x, speed_y):
        map = self.main_gameplay.map.return_map()

        for y in range(self.main_gameplay.map.map_size[1]):
            for x in range(self.main_gameplay.map.map_size[0]):
                other = map[y][x]

                if other and other.type != "forcefield":
                    if pg.sprite.collide_rect(self, other):
                        # Right
                        if speed_x > 0:
                            self.rect.right = other.rect.left

                        # Left
                        if speed_x < 0:
                            self.rect.left = other.rect.right

                        # Up
                        if speed_y < 0:
                            self.rect.top = other.rect.bottom
                            self.vel = (self.vel[0], 0)

                        # Down
                        if speed_y > 0:
                            self.rect.bottom = other.rect.top
                            self.on_ground = True
                            self.vel = (self.vel[0], 0)

                            if other.type == "jumppad":
                                self.vel = (self.vel[0], self.vel[1] - other.force)
                        else:
                            self.on_ground = False
