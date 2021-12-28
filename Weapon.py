# Класс оружий. Тип пуль, урон, статы и т.д. тут.

# Импорт библиотек
import math
import random

import pygame as pg

import Bullet


class Weapon(pg.sprite.Sprite):
    def __init__(self, app, state, player,
                 bullets_per_second=50, damage=5,
                 speed=10, bullets_per_time=1,
                 distance=1000, spread=None,
                 ammo=None, reload_time=1, bullet_type="phys",
                 image=None, shot_type='click', source="player"):

        pg.sprite.Sprite.__init__(self)
        if spread is None:
            spread = [0, 0.2, 0, 15, 1]
        if ammo is None:
            ammo = [30, 30, 100, 100]
        self.app = app
        self.state = state
        self.player = player
        self.image_path = image
        self.source = source

        self.selected = False
        if self.image_path:
            self.image = pg.image.load(self.image_path)
            self.image.set_colorkey(self.image.get_at((0, 0)))
        else:
            self.image = None
        self.rect = pg.Rect(0, 0, 0, 0)

        self.bullet_type = bullet_type  # phys (физ урон), exp (взрыв), en (энергия [wip])

        self.bullet_vector = (0, 0)

        self.bullets_per_second = bullets_per_second
        self.shoot_cd = [0, 1 / self.bullets_per_second]  # Время между выстрелами. Слева действующие числа,
        # справа число для сброса

        self.damage = damage
        self.spread = spread  # Разброс в градусах. 0 текущий, 1 дельта, 2 мин, 3 макс, 4 время до сброса
        self.speed = speed
        self.bullets_per_time = bullets_per_time
        self.distance = distance

        self.ammo = ammo  # 0 в обойме, 1 макс в обойме, 2 в запасе, 3 макс в запасе
        self.shot_type = shot_type
        self.reloading = False
        self.reload_time = [0, reload_time]  # 0 текущее, 1 макс

        # slot: [weapon, name, slot, lvl (1,2,3),
        # [(Название параметра, переменная для изменения, [число на которе умножить, lvl1, lvl2, lvl3]), (), ()...]
        # Пустой слот: WeaponMod(self, "Stock", [0, 0], "optic")
        # Пример: WeaponMod(self, "Red dot", [0, 3], "optic",
        #                                         [("Spread", "self.weapon.spread[3]", [0.5, 0.5, 0.5])], 100)
        self.mods = {"optic": WeaponMod(self, "Stock", [0, 0], "optic"),
                     "muzzle": WeaponMod(self, "Stock", [0, 0], "muzzle"),
                     "underbarrel": WeaponMod(self, "Stock", [0, 0], "underbarrel"),
                     "stock": WeaponMod(self, "Stock", [0, 0], "stock"),
                     "magazine": WeaponMod(self, "Stock", [0, 0], "magazine")}
        for key in self.mods.keys():
            if self.mods[key]:
                self.mods[key].apply()

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            if self.image:
                self.image = pg.transform.scale(self.image, (int(self.state.map.block_size[0] * 2),
                                                             int(self.state.map.block_size[0] * 2)))
                self.rect = self.image.get_rect()
            else:
                self.rect = pg.Rect(0, 0,
                                    int(self.state.map.block_size[0]), int(self.state.map.block_size[0] / 2))

        # IMAGE
        self.rect.x, self.rect.y = self.player.rect.centerx - self.rect.width / 2, \
                                   self.player.rect.centery
        if self.image:
            self.rect.y -= self.image.get_height() / 2

        self.shoot_cd[0] -= self.app.clock.get_time() / 1000
        self.spread_op()
        if self.selected:
            self.reload()

            if self.reloading:
                self.reload_time[0] -= self.app.clock.get_time() / 1000

            else:
                if self.shot_type == 'click' and pg.mouse.get_pressed(3)[0]:
                    self.bullet_vector = pg.mouse.get_pos()
                    self.shoot()
                    self.reload_time[0] = self.reload_time[1]

        else:
            self.reloading = False

        self.ammo[2] = max(min(self.ammo[2], self.ammo[3]), 0)

    def render(self):
        if self.image:
            angle = math.degrees(self.get_rot_pos(self.rect.center)[1])

            image = self.image
            if -180 <= angle <= -90 or 90 <= angle <= 180:
                image = pg.transform.flip(self.image, False, True)

            image = pg.transform.rotate(image, -angle)

            self.app.screen.blit(image, image.get_rect(center=self.rect.center))

            self.app.screen.blit(image, image.get_rect(center=self.rect.center))

        else:
            pass
            pg.draw.rect(self.app.screen, (0, 0, 255), self.rect)

    def spread_op(self):
        if -self.shoot_cd[0] + self.shoot_cd[1] > self.spread[4]:
            self.spread[0] -= self.spread[1]

        if self.spread[0] < self.spread[2]:
            self.spread[0] = self.spread[2]

        if self.spread[0] > self.spread[3]:
            self.spread[0] = self.spread[3]

    def shoot(self):
        if self.shoot_cd[0] <= 0 and self.ammo[0] > 0:
            self.ammo[0] -= 1
            for _ in range(self.bullets_per_time):
                self.state.bullets.add(Bullet.Bullet(self.app, self.state, self, self.source, self.bullet_vector))

                self.shoot_cd[0] = self.shoot_cd[1]
                self.spread[0] += self.spread[1]

            self.reload_time[0] = self.reload_time[1]

    def reload(self):
        if (pg.key.get_pressed()[pg.K_r] or self.ammo[0] == 0) and \
                self.ammo[0] != self.ammo[1] and \
                self.reload_time[0] >= 0 and \
                not self.reloading and self.ammo[2]:
            self.reloading = True

        if self.reloading and self.reload_time[0] <= 0:
            picked_ammo = min(self.ammo[1] - self.ammo[0], self.ammo[2])
            self.ammo[2] -= picked_ammo
            self.ammo[0] += picked_ammo
            self.reloading = False

    def get_rot_pos(self, pos, spread=False):
        mouse_x, mouse_y = pg.mouse.get_pos()

        distance_x = mouse_x - pos[0]
        distance_y = mouse_y - pos[1]

        angle = math.atan2(distance_y, distance_x)
        if self.spread[0] != 0 and spread:
            angle += math.radians(random.randint(int(-self.spread[0] * 100),
                                                 int(self.spread[0] * 100)) / 100)

        return (self.rect.centerx + math.cos(angle) * self.rect.width / 2,
                self.rect.centery + math.sin(angle) * self.rect.width / 2), angle

    def get_save_data(self):
        mods = {}
        for k in self.mods.keys():
            mods[k] = self.mods[k].get_save_data()

        data = [self.bullets_per_second, self.damage,
                self.speed, self.bullets_per_time,
                self.distance, self.spread,
                self.ammo, self.reload_time[1], self.bullet_type,
                self.image_path, self.shot_type, self.source, mods]

        return data

    def reload_image(self, image_path):
        if image_path:
            self.image = pg.image.load(image_path)
            self.image.set_colorkey(self.image.get_at((0, 0)))
        else:
            self.image = None
        self.image_path = image_path

        if self.image:
            self.image = pg.transform.scale(self.image, (int(self.state.map.block_size[0] * 2),
                                                         int(self.state.map.block_size[0] * 2)))
            self.rect = self.image.get_rect()
        else:
            self.rect = pg.Rect(0, 0,
                                int(self.state.map.block_size[0]), int(self.state.map.block_size[0] / 2))

    def upgrade(self, mod_ind):
        mod = self.mods[mod_ind]
        if mod:
            if mod.lvl[0] < mod.lvl[1] and mod.cost <= self.player.money:
                mod.upgrade_lvl()
            # mod.print()
        else:
            print("NO MOD IN " + mod_ind)


class WeaponMod:
    def __init__(self, weapon, name, lvl, slot="optic", vars_mods=None, cost=None):
        if cost is None:
            cost = 0
        self.cost = cost
        if vars_mods is None:
            vars_mods = []
        self.weapon = weapon
        self.lvl = lvl
        self.slot = slot
        self.vars_mods = vars_mods
        self.name = name

    def apply(self):
        for name, var, value in self.vars_mods:
            if self.lvl[0] > 1:
                exec(var + " = " + var + " / " + str(value[self.lvl[0] - 2]) + " * " + str(value[self.lvl[0] - 1]))
            elif self.lvl[0] > 0:
                exec(var + " = " + var + " * " + str(value[self.lvl[0] - 1]))

        self.cost *= 2 ** self.lvl[0]

    def upgrade_lvl(self):
        self.lvl[0] += 1
        self.weapon.player.money -= self.cost
        for name, var, value in self.vars_mods:
            if self.lvl[0] > 1:
                exec(var + " = " + var + " / " + str(value[self.lvl[0] - 2]) + " * " + str(value[self.lvl[0] - 1]))
            elif self.lvl[0] > 0:
                exec(var + " = " + var + " * " + str(value[self.lvl[0] - 1]))

        self.cost *= 2

    def print(self):
        print(self.name, self.slot, self.lvl, self.vars_mods, self.cost)

    def get_effect(self):
        data = ""
        if self.lvl != [0, 0]:
            for name, var, value in self.vars_mods:
                data += str(self.cost) + "$     " + name + "    " + \
                        " / ".join(list(map(str, [str(int(i * 100)) + "%" for i in value])))
                data += "    "
        else:
            data += "Slot Empty"

        return data

    def get_save_data(self):
        return [self.name, self.lvl, self.slot, self.vars_mods, self.cost]