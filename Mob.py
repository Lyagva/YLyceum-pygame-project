import math

import numpy as np
import pygame as pg

import Weapon
from Functions import *


class Mob(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, pos):
        pg.sprite.Sprite.__init__(self)

        self.app = app
        self.main_gameplay = main_gameplay

        self.image = pg.Surface((round(self.main_gameplay.map.block_size[0] * 0.8), round(self.main_gameplay.map.block_size[1] * 1.6)))
        self.image.fill(pg.Color('green'))

        self.x, self.y = pos
        self.rect = pg.Rect(0, 0, 0, 0)
        self.type = 'mob'

        self.health = [100, 100]  # 0 текущее хп, 1 макс хп

        self.weapons = [Weapon.Weapon(self.app, self.main_gameplay, self,
                                      spread=[0, 0.3, 0, 20, 4], ammo=[500, 500, 20000, 20000],
                                      reload_time=5, bullet_type="exp", shot_type='auto', source="mob")]
        self.selected_weapon = 0

        self.gravity = 10
        self.speed = (100, 20)
        self.vel = (0, 0)  # x, y
        self.on_ground = False

        self.visible = 600  # расстояние видимости

        # Raycasting
        self.line_to_player = [[self.rect.center, self.main_gameplay.player.rect.center], np.array([])]

        self.turn_to = 'left'  # сторона поворота
        self.max_time_jump = self.app.FPS / 5  # 1/5 секунда
        self.time_of_jump = 0
        self.go_to_left, self.go_to_right, self.go_jump = False, False, False

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x, self.y,
                                self.main_gameplay.map.block_size[0] * 0.8,
                                self.main_gameplay.map.block_size[1] * 1.6)

        # update visible
        if self.line_to_player[1] or \
                get_hypotenuse(self.line_to_player[0][0][0], self.line_to_player[0][1][0],
                               self.line_to_player[0][0][1], self.line_to_player[0][1][1]) > self.visible or \
                self.main_gameplay.player.rect.x < self.rect.x if self.turn_to == 'right' else self.main_gameplay.player.rect.x > self.rect.x:
            # не видит
            self.image.fill(pg.Color('green'))
        else:
            self.image.fill(pg.Color('red'))
            self.weapons[self.selected_weapon].bullet_vector = self.line_to_player[0][1]
            self.weapons[self.selected_weapon].shoot()

        # update weapon
        self.weapons[self.selected_weapon].selected = True

        # update commands
        self.go_jump = False
        # self.go_to_right = True

        # update moves
        self.movement()

        # update Raycasting
        self.update_raycast()
        [w.update() for w in self.weapons]

    def update_raycast(self):
        easy_map = [obg for lst in self.main_gameplay.map.map for obg in lst if obg is not None]
        x, y, x1, y1 = self.rect.centerx, self.rect.centery, self.main_gameplay.player.rect.centerx, self.main_gameplay.player.rect.centery
        self.line_to_player = [[(x, y), (x1, y1)], lineRectIntersectionPoints([(x, y), (x1, y1)], easy_map)]

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

        # update turn
        if self.vel[0] > 0:
            self.turn_to = 'right'
        elif self.vel[0] < 0:
            self.turn_to = 'left'

        # Horizontal coll
        self.rect.x += self.vel[0]
        self.wall_collision(self.vel[0], 0)

        # Vertical coll
        self.rect.y += self.vel[1]
        self.wall_collision(0, self.vel[1])

    def render(self):
        self.app.screen.blit(self.image, (self.rect.x, self.rect.y))

        # Глаза
        pg.draw.circle(self.app.screen, pg.Color("white"),
                       (self.rect.centerx + 20 * (1 if self.turn_to == "right" else -1),
                        self.rect.centery - self.rect.height * 0.3), 10)

        # оружие
        self.weapons[self.selected_weapon].render()

        pg.draw.circle(self.app.screen, pg.Color('red'), self.rect.center, self.visible, 4)

        # raycast
        pg.draw.line(self.app.screen, pg.Color('white'), self.line_to_player[0][0], self.line_to_player[0][1], 1)
        for point in self.line_to_player[1]:
            pg.draw.circle(self.app.screen, pg.Color('white'), point, 4)

        # charts

        # health
        self.draw_chart(self.rect.x - self.rect.width // 2, self.rect.y - 30, 2 * self.rect.width, 20, self.health[0], self.health[1], 'row')
        # charged bullets
        self.draw_chart(self.rect.x - self.rect.width // 2, self.rect.y - 30 - 10 - self.rect.height, 20, self.rect.height, self.weapons[self.selected_weapon].ammo[0], self.weapons[self.selected_weapon].ammo[1], 'col')
        # bullets in case
        self.draw_chart(self.rect.x - self.rect.width // 2 + 20 + 10, self.rect.y - 30 - 10 - self.rect.height, 20, self.rect.height, self.weapons[self.selected_weapon].ammo[2], self.weapons[self.selected_weapon].ammo[3], 'col')

    def get_damage(self, dmg):
        self.health[0] -= dmg

    def draw_chart(self, x, y, width, height, pct, max_pct, row_or_col):
        if pct < 0:
            pct = 0

        fill = pct / max_pct * width if row_or_col == 'row' else pct / max_pct * height
        if pct / max_pct >= 0.75:
            color = pg.Color('Green')
        elif pct / max_pct >= 0.5:
            color = pg.Color('Yellow')
        elif pct / max_pct >= 0.2:
            color = pg.Color('Red')
        else:
            color = pg.Color('DarkRed')

        outline_rect = pg.Rect(x, y, width, height)
        if row_or_col == 'row':
            fill_rect = pg.Rect(x, y, fill, height)
        else:
            fill_rect = pg.Rect(x, y, width, fill)
        pg.draw.rect(self.app.screen, color, fill_rect)
        pg.draw.rect(self.app.screen, pg.Color('white'), outline_rect, 2)

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
