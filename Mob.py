import pygame as pg
import time
import random as rd

import PickUp
import Weapon
from Functions import *


class Mob(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, map, pos):
        pg.sprite.Sprite.__init__(self)

        self.app = app
        self.main_gameplay = main_gameplay
        self.map = map

        self.image = pg.Surface((round(self.map.block_size[0] * 0.8), round(self.map.block_size[1] * 1.6)))
        self.image.fill(pg.Color('green'))

        self.x, self.y = pos
        self.rect = pg.Rect(0, 0, 0, 0)
        self.type = 'mob'
        self.is_death = False
        self.drop = rd.choice(self.app.loot_table)

        self.health = [100, 100]  # 0 текущее хп, 1 макс хп

        rd_wp = rd.choice(self.app.weapons_table)
        self.weapons = [Weapon.Weapon(self.app, self.main_gameplay, self,

                                      bullets_per_second=rd_wp[0], damage=rd_wp[1],
                                      speed=rd_wp[2], bullets_per_time=rd_wp[3],
                                      distance=rd_wp[4], spread=rd_wp[5],
                                      ammo=rd_wp[6], reload_time=rd_wp[7], bullet_type=rd_wp[8],
                                      image=rd_wp[9],

                                      shot_type='auto', source="mob")]
        self.selected_weapon = 0

        # logic of move
        self.is_wall = False
        self.jump_counter = 0

        self.gravity = 10
        self.speed = (100, 20)
        self.vel = (0, 0)  # x, y
        self.on_ground = False

        self.visible = 600  # расстояние видимости если он смотрит на игрока
        self.absolute_visible = 100  # на этом расстоянии бот видит игрока полюбому
        self.player_is_visible = False

        # Raycasting
        self.line_to_player = [
            [[self.rect.center, self.main_gameplay.player.rect.center], []]
        ]

        self.turn_to = 'right'  # сторона поворота
        self.max_time_jump = self.app.FPS / 5  # 1/5 секунда
        self.time_of_jump = 0
        self.go_to_left, self.go_to_right, self.go_jump = False, False, False

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x, self.y,
                                self.map.block_size[0] * 0.8,
                                self.map.block_size[1] * 1.6)

        # check live
        if self.health[0] <= 0:
            self.is_death = True

        if self.is_death:
            self.main_gameplay.stats["kills"] += 1
            self.made_pickup_from_drop()
            self.kill()
            return

        # update visible
        # проверяем сначала абсолютную видимость потом визуальную если ничего не подходит то не видит
        if (not all(list(map(lambda line: 1 if line[1] else 0, self.line_to_player))) and any(list(map(lambda line: 1 if get_hypotenuse(line[0][0][0], line[0][1][0], line[0][0][1], line[0][1][1]) <= self.absolute_visible else 0, self.line_to_player)))) or \
                (not all(list(map(lambda line: 1 if line[1] else 0, self.line_to_player))) and any(list(map(lambda line: 1 if get_hypotenuse(line[0][0][0], line[0][1][0], line[0][0][1], line[0][1][1]) <= self.visible else 0, self.line_to_player))) and ((self.main_gameplay.player.rect.x <= self.rect.x if self.turn_to == 'left' else self.main_gameplay.player.rect.x >= self.rect.x) or self.player_is_visible)):
            self.player_is_visible = True
        else:
            self.player_is_visible = False

        # update weapon
        self.weapons[self.selected_weapon].selected = True
        if not self.player_is_visible and self.weapons[self.selected_weapon].ammo[0] < \
                self.weapons[self.selected_weapon].ammo[1] / 2:
            # авто перезарядка если не видит игрока и в обойме меньше половины патронов
            self.weapons[self.selected_weapon].reload()

        # update commands
        if self.player_is_visible:
            self.image.fill(pg.Color('red'))
            if self.rect.centerx < self.main_gameplay.player.rect.centerx and self.turn_to != 'right':
                # print('поворот к игроку право')
                self.turn_to = 'right'
            elif self.rect.centerx > self.main_gameplay.player.rect.centerx and self.turn_to != 'left':
                # print('поворот к игроку лево')
                self.turn_to = 'left'

            self.weapons[self.selected_weapon].bullet_vector = self.main_gameplay.player.rect.center
            self.weapons[self.selected_weapon].shoot()
            # стоит для стрельбы
            self.go_jump, self.go_to_right, self.go_to_left = False, False, False
        else:
            self.image.fill(pg.Color('green'))
            self.weapons[self.selected_weapon].bullet_vector = ((self.rect.centerx + 10 if self.turn_to == 'right'
                                                                 else self.rect.centerx - 10), self.rect.centery)

            # print(self.pos_be[0], self.rect.x)
            if not self.is_wall:  # если нет препятствий
                # print('нет препятствий')
                if self.turn_to == 'left':
                    self.go_to_left = True
                elif self.turn_to == 'right':
                    self.go_to_right = True
            else:
                # print('препятствия')
                if self.jump_counter <= self.app.FPS:
                    # если прыгаем меньше сек то еще пытаемся пройти через препятствие
                    self.go_jump = True
                    self.jump_counter += 1
                    if self.turn_to == 'left':
                        self.go_to_left = True
                    elif self.turn_to == 'right':
                        self.go_to_right = True
                else:  # прыгали но снова препятствие
                    self.jump_counter = 0
                    if self.turn_to == 'left':
                        self.go_to_right = True
                    elif self.turn_to == 'right':
                        self.go_to_left = True

        # update moves
        self.movement()

        self.go_jump, self.go_to_right, self.go_to_left = False, False, False

        # update Raycasting
        self.update_raycast()
        [w.update() for w in self.weapons]

    def update_raycast(self):
        start = time.time()

        easy_map = [obg for lst in self.map.map for obg in lst if obg is not None]

        self.line_to_player = [
            [[self.rect.center, self.main_gameplay.player.rect.center],
             lineRectIntersectionPoints([self.rect.center, self.main_gameplay.player.rect.center], easy_map)]
        ]
        end = time.time()
        #print('time of update raycast', end - start)

    def movement(self):
        dt = self.app.clock.get_fps()

        self.is_wall = False

        self.vel = (0, self.vel[1])

        # Right
        if self.go_to_right:
            self.vel = (self.vel[0] + self.speed[0] / dt, self.vel[1])

        # Left
        if self.go_to_left:
            self.vel = (self.vel[0] - self.speed[0] / dt, self.vel[1])

        # Jump
        if self.go_jump and self.time_of_jump < self.max_time_jump:
            self.on_ground = False
            self.vel = (self.vel[0], self.vel[1] - self.speed[1] / dt)

        #  GRAVITI
        self.vel = (self.vel[0], self.vel[1] + self.gravity / dt)

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

        # update turn
        if self.vel[0] > 0 and self.turn_to != 'right':
            # print('поворот ходьба право')
            self.turn_to = 'right'
        elif self.vel[0] < 0 and self.turn_to != 'left':
            # print('поворот ходьба лево')
            self.turn_to = 'left'

    def render(self):
        self.app.screen.blit(self.image, (self.rect.x, self.rect.y))

        # Глаза
        pg.draw.circle(self.app.screen, pg.Color("white"),
                       (self.rect.centerx + 20 * (1 if self.turn_to == "right" else -1),
                        self.rect.centery - self.rect.height * 0.3), 10)

        # оружие
        self.weapons[self.selected_weapon].render()

        # visible
        pg.draw.circle(self.app.screen, pg.Color('red'), self.rect.center, self.visible, 4)
        pg.draw.circle(self.app.screen, pg.Color('Yellow'), self.rect.center, self.absolute_visible, 4)

        # raycast
        for line in self.line_to_player:
            pg.draw.line(self.app.screen, pg.Color('white'), line[0][0], line[0][1], 1)
            for point in line[1]:
                pg.draw.circle(self.app.screen, pg.Color('white'), point, 4)

        # charts
        # health
        self.draw_chart(self.rect.x - self.rect.width // 2, self.rect.y - 30, 2 * self.rect.width, 20, self.health[0],
                        self.health[1], 'row')
        # charged bullets
        self.draw_chart(self.rect.x - self.rect.width // 2, self.rect.y - 30 - 10 - self.rect.height, 20,
                        self.rect.height, self.weapons[self.selected_weapon].ammo[0],
                        self.weapons[self.selected_weapon].ammo[1], 'col')
        # bullets in case
        self.draw_chart(self.rect.x - self.rect.width // 2 + 20 + 10, self.rect.y - 30 - 10 - self.rect.height, 20,
                        self.rect.height, self.weapons[self.selected_weapon].ammo[2],
                        self.weapons[self.selected_weapon].ammo[3], 'col')

    def get_damage(self, dmg, pos_dmg):
        self.health[0] -= dmg
        if pos_dmg[0] < self.rect.centerx and not self.player_is_visible and self.turn_to != 'left':
            # если дамаг нанесен слева, если не видит игрока и если уже не повернут в нужную сторону
            # print('поворот дамаг лево')
            self.turn_to = 'left'

        elif pos_dmg[0] > self.rect.centerx and not self.player_is_visible and self.turn_to != 'right':
            # если дамаг нанесен справа, если не видит игрока и если уже не повернут в нужную сторону
            # print('поворот дамаг право')
            self.turn_to = 'right'

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
        map = self.map.return_map()

        for y in range(self.map.map_size[1]):
            for x in range(self.map.map_size[0]):
                other = map[y][x]

                if other and other.type not in ["forcefield", "lever", "prop"]:
                    if pg.sprite.collide_rect(self, other):
                        # Right
                        if speed_x > 0:
                            self.rect.right = other.rect.left
                            self.vel = (0, self.vel[1])
                            self.is_wall = True

                        # Left
                        if speed_x < 0:
                            self.rect.left = other.rect.right
                            self.vel = (0, self.vel[1])
                            self.is_wall = True

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

    def made_pickup_from_drop(self):
        if self.drop:
            if self.drop[0] == 'pickup_ammo':
                self.main_gameplay.items.add(PickUp.ItemAmmo(self.app, self.main_gameplay, self.map,
                                                             (self.rect.x / self.map.block_size[0],
                                                              self.rect.y / self.map.block_size[0]),
                                                             image=self.drop[1],
                                                             ammo=int(self.drop[2])))
            elif self.drop[0] == 'pickup_medkit':
                self.main_gameplay.items.add(PickUp.ItemMedKit(self.app, self.main_gameplay, self.map,
                                                               (self.rect.x / self.map.block_size[0],
                                                                self.rect.y / self.map.block_size[0]),
                                                               image=self.drop[1], dhp=int(self.drop[2])))
            elif self.drop[0] == 'pickup_grenade':
                self.main_gameplay.items.add(PickUp.ItemGrenade(self.app, self.main_gameplay, self.map,
                                                                (self.rect.x / self.map.block_size[0],
                                                                 self.rect.y / self.map.block_size[0]),
                                                                image=self.drop[1]))
