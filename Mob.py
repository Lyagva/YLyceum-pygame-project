import random


import pygame as pg
import Weapon


class Mob(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, pos):
        pg.sprite.Sprite.__init__(self)

        self.app = app
        self.main_gameplay = main_gameplay

        self.x, self.y = pos
        self.rect = pg.Rect(0, 0, 0, 0)
        self.type = 'mob'

        self.health = [100, 100]  # 0 текущее хп, 1 макс хп

        self.weapons = [Weapon.Weapon(self.app, self.main_gameplay, self, ammo=[500, 500, 20000, 20000], bullet_type="exp")]
        self.selected_weapon = 0

        self.gravity = 10
        self.speed = (100, 20)
        self.vel = (0, 0)  # x, y
        self.on_ground = False

        self.max_time_jump = self.app.clock.get_time()  # 1 секунда
        self.time_of_jump = 0
        self.go_to_left, self.go_to_right, self.go_jump = False, False, False

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x,
                                self.y,
                                self.main_gameplay.map.block_size[0] * 0.8,
                                self.main_gameplay.map.block_size[1] * 1.6)

        self.go_jump = True

        self.movement()

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
        self.rect.y += round(self.vel[1], 2)
        self.wall_collision(0, self.vel[1])

        print(self.rect.x, self.rect.y)

    def render(self):
        pg.draw.rect(self.app.screen, (255, 255, 255), self.rect)

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

