# Класс игрока. Движение, прицеливание, стрельба и т.д. будут тут.

# Импорт библиотек
import math

import pygame as pg

# Импорт классов
import Grenade
import Weapon
from PickUp import ItemWeapon


class Player(pg.sprite.Sprite):
    def __init__(self, app, state):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.money = 10000

        # Движение
        self.speed = (500, 20)  # Скорость и сила прыжка
        self.gravity = 10
        self.vel = (0, 0)  # Смещение за один кадр

        # RUN
        self.running = False
        self.running_speed_mod = 1.5

        self.rect = pg.Rect(0, 0, 0, 0)

        # JUMP
        self.on_ground = False
        self.jump_cooldown = [0, 0.5]  # Первое - время, которое изменяется. А второе - время к ресету
        self.jump_fuel = [0, 0.5, 1]  # Текущее, дельта, кд до запуска, макс

        # WEAPON
        self.weapons = [Weapon.Weapon(self.app, self.state, self, ammo=[5000, 5000, 20000, 20000],
                                      bullet_type="exp", bullets_per_second=40, image="images/weapons/rpg.png"),
                        Weapon.Weapon(self.app, self.state, self, bullets_per_second=4,
                                      bullets_per_time=5,
                                      spread=[0, 0, 20, 20, 0], ammo=[10, 10, 100, 100]),
                        Weapon.Weapon(self.app, self.state, self, bullets_per_second=1, bullets_per_time=1,
                                      spread=[0, 0, 0, 0, 0], damage=100, ammo=[1, 1, 10, 10], bullet_type="exp")]

        self.selected_weapon = 0

        self.health = [100, 100]  # 0 текущее хп, 1 макс хп
        self.grenades = [3, 3]  # 0 текущее, 1 макс
        self.grenade_pressed = False
        self.drop_pressed = False
        self.angle = 0

        self.font = pg.font.SysFont("sans", 24)
        self.upgrades = {"Health": [1, 5, 100, 25, "+"],
                         "Grenades Count": [1, 5, 100, 1, "+"],
                         "Speed": [1, 5, 100, 1.1, "*"],
                         "Jump Fuel": [1, 3, 100, 0.5, "+"]}  # Name: [level, max_level, cost, delta, op(plus, mul)]

    def update(self):
        buttons = pg.key.get_pressed()
        self.health[0] = min(max(self.health[0], -100000), self.health[1])

        if self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.rect.x,
                                self.rect.y,
                                self.state.map.block_size[0] * 0.8,
                                self.state.map.block_size[1] * 1.6)

        self.weapon_op()
        self.grenade_op()
        self.jump_cooldown[0] -= self.app.clock.get_time() / 1000
        self.movement()
        [w.update() for w in self.weapons]

        if buttons[pg.K_F2]:
            self.money += 1

        if self.health[0] <= 0:
            self.die()

    def render(self):
        pg.draw.rect(self.app.screen, (255, 255, 255), self.rect)
        self.weapons[self.selected_weapon].render()

        # Прицел & Курсор
        mouse = pg.mouse.get_pos()
        distance_x = mouse[0] - self.rect.centerx
        distance_y = mouse[1] - self.rect.centery
        self.angle = math.atan2(distance_y, distance_x)

        d = ((mouse[0] - self.rect.x + math.cos(self.angle) * self.weapons[self.selected_weapon].rect.width) ** 2 +
             (mouse[1] - self.rect.y + math.sin(self.angle) * self.weapons[self.selected_weapon].rect.height) ** 2)\
            ** 0.5
        r = math.tan(math.radians(self.weapons[self.selected_weapon].spread[0])) * d
        pg.draw.circle(self.app.screen, (255, 255, 255), mouse, r, width=2)

        pg.draw.circle(self.app.screen, (255, 255, 255), mouse, 10, width=2)

        # Полёт
        text = self.font.render("Jet fuel: " + str(round(self.jump_fuel[0] * 100)), True, (255, 64, 64))
        self.app.screen.blit(text, (10, 10))

        # Оружие
        text = self.font.render("Weapon: " + str(self.selected_weapon + 1), True, (255, 64, 64))
        self.app.screen.blit(text, (10, 30))

        # Здоровье
        text = self.font.render("Health: " + str(self.health[0]) + "/" + str(self.health[1]),
                                True, (0, 255, 0))

        self.app.screen.blit(text, (10,
                                    self.app.screen_size[1] - text.get_height() - 30))

        # Патроны
        text = self.font.render(("Reloading... " if self.weapons[self.selected_weapon].reloading else "") +
                                str(self.weapons[self.selected_weapon].ammo[0]) + "/" +
                                str(self.weapons[self.selected_weapon].ammo[1]) + " (" +
                                str(self.weapons[self.selected_weapon].ammo[2]) + ")",
                                True, (255, 64, 64))

        self.app.screen.blit(text, (self.app.screen_size[0] - text.get_width() - 10,
                                    self.app.screen_size[1] - text.get_height() - 30))

        # Гранаты
        text = self.font.render("Grenades: " + str(self.grenades[0]) + "/" + str(self.grenades[1]),
                                True, (0, 255, 0))

        self.app.screen.blit(text, (10,
                                    self.app.screen_size[1] - text.get_height() - 30 - text.get_height()))

        # Money
        text = self.font.render("Money: " + str(self.money), True, (241, 196, 15))
        self.app.screen.blit(text, (self.app.screen_size[0] - 10 - text.get_width(), 30))

    def movement(self):
        buttons = pg.key.get_pressed()
        dt = self.app.clock.get_time() / 1000

        self.vel = (0, self.vel[1])
        # Right
        if buttons[pg.K_d]:
            self.vel = (self.vel[0] + self.speed[0] * dt,
                        self.vel[1])
        # Left
        if buttons[pg.K_a]:
            self.vel = (self.vel[0] - self.speed[0] * dt,
                        self.vel[1])

        # Run
        if pg.key.get_pressed()[pg.K_LSHIFT]:
            self.running = True
        else:
            self.running = False

        if self.running:
            self.vel = (self.vel[0] * self.running_speed_mod, self.vel[1])

        is_on_stairs = pg.sprite.spritecollide(self, self.state.stairs, False)
        # Jump or stairs
        if is_on_stairs and not buttons[pg.K_SPACE]:
            self.vel = (self.vel[0], 0)
            #  скорость как по x
            if buttons[pg.K_w]:
                self.vel = (self.vel[0], self.vel[1] - self.speed[0] * dt)
            if buttons[pg.K_s]:
                self.vel = (self.vel[0], self.vel[1] + self.speed[0] * dt)

        if buttons[pg.K_SPACE] and self.jump_fuel[0] > 0:
            self.on_ground = False
            self.jump_fuel[0] -= self.jump_fuel[1] * dt
            self.vel = (self.vel[0], self.vel[1] - self.speed[1] * dt)

        if self.on_ground:
            self.jump_fuel[0] += self.jump_fuel[1] * dt

        self.jump_fuel[0] = min(max(self.jump_fuel[0], 0), self.jump_fuel[2])

        # Gravity
        if not is_on_stairs:
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

                if other and other.type not in ["forcefield", "lever", "prop"]:
                    if pg.sprite.collide_rect(self, other):
                        if other.type == 'danger_block':
                            self.get_damage(other.damage)
                            if not other.is_collide:
                                continue

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

    def weapon_op(self):
        buttons = pg.key.get_pressed()
        events = self.app.events

        self.weapons[self.selected_weapon].selected = False

        if buttons[pg.K_i]:
            if len(self.weapons) > 1 and not self.drop_pressed:
                self.drop_pressed = True
                self.state.items.add(ItemWeapon(self.app, self.state, self.state.map, self.rect.center,
                                                self.weapons[self.selected_weapon]))
                self.weapons.remove(self.weapons[self.selected_weapon])
                self.selected_weapon -= 1
        else:
            self.drop_pressed = False

        # Смена на колёсико
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.selected_weapon += 1
                if e.button == 5:
                    self.selected_weapon -= 1

        if buttons[pg.K_1]:
            self.selected_weapon = 0
        elif buttons[pg.K_2]:
            self.selected_weapon = 1
        elif buttons[pg.K_3]:
            self.selected_weapon = 2

        self.selected_weapon = self.selected_weapon % len(self.weapons)
        self.weapons[self.selected_weapon].selected = True

    def grenade_op(self):
        buttons = pg.key.get_pressed()

        if buttons[pg.K_g]:
            if self.grenades[0] > 0 and not self.grenade_pressed:
                self.grenade_pressed = True
                self.grenades[0] -= 1
                self.state.grenades.add(Grenade.Grenade(self.app, self.state))
        else:
            self.grenade_pressed = False

    def get_damage(self, dmg):
        self.health[0] -= dmg

    def set_pos(self, pos):
        self.rect.x, self.rect.y = pos

    def get_save_data(self):
        weapons = [w.get_save_data() for w in self.weapons]
        data = [self.health, self.grenades, weapons, self.money, self.upgrades]

        return data

    def make_upgrade(self, upg_id):
        upgrade = self.upgrades[upg_id]
        if self.money >= upgrade[2] and upgrade[0] < upgrade[1]:
            self.money -= upgrade[2]
            upgrade[0] += 1
            upgrade[2] *= 2
            if upg_id == "Health":
                self.health[1] = eval(str(self.health[1]) +
                                      str(self.upgrades["Health"][4]) +
                                      str(self.upgrades["Health"][3]))
                self.health[0] = self.health[1]
            if upg_id == "Grenades Count":
                self.grenades[1] = eval(str(self.grenades[1]) +
                                        str(self.upgrades["Grenades Count"][4]) +
                                        str(self.upgrades["Grenades Count"][3]))
                self.grenades[0] = self.grenades[1]
            if upg_id == "Speed":
                self.speed = (eval(str(self.speed[0]) +
                                   str(self.upgrades["Speed"][4]) +
                                   str(self.upgrades["Speed"][3])), self.speed[1])
            if upg_id == "Jump Fuel":
                self.jump_fuel[2] = eval(str(self.jump_fuel[2]) +
                                         str(self.upgrades["Jump Fuel"][4]) +
                                         str(self.upgrades["Jump Fuel"][3]))

    def reload_upgrades(self):
        self.health[0] = self.health[1]
        self.grenades[0] = self.grenades[1]

        self.jump_fuel = [0, 0.5, 1]
        self.jump_fuel[2] = eval(str(self.jump_fuel[2]) +
                                 (str(self.upgrades["Jump Fuel"][4]) +
                                  str(self.upgrades["Jump Fuel"][3])) * (self.upgrades["Jump Fuel"][0] - 1))

        self.speed = (500, 20)
        self.speed = (eval(str(self.speed[0]) +
                           (str(self.upgrades["Speed"][4]) +
                            str(self.upgrades["Speed"][3])) * (self.upgrades["Speed"][0] - 1)), self.speed[1])

    def reload(self):
        self.rect.topleft = (0, 0)
        for w in self.weapons:
            w.ammo[0] = w.ammo[1]
            w.ammo[2] = w.ammo[3]

        self.reload_upgrades()
        self.jump_fuel[0] = self.jump_fuel[2]

    def die(self):
        self.health[0] = self.health[1]
        self.weapons[0].ammo[2] = self.weapons[0].ammo[3]
        self.state.map.read_file()
        self.state.stats["kills"] = 0
        self.state.stats["time"] = 0