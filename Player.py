# Класс игрока. Движение, прицеливание, стрельба и т.д. будут тут.

# Импорт библиотек
import math

import pygame as pg

# Импорт классов
import Grenade
import Weapon


class Player(pg.sprite.Sprite):
    def __init__(self, app, state, pos):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.x, self.y = pos
        self.state = state

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
        self.jump_fuel = [0, 0.5, 1, 1]

        # WEAPON
        self.weapons = [Weapon.Weapon(self.app, self.state, self, ammo=[5000, 5000, 20000, 20000],
                                      bullet_type="exp", bullets_per_second=40),
                        Weapon.Weapon(self.app, self.state, self, bullets_per_second=4,
                                      bullets_per_time=5,
                                      spread=[0, 0, 20, 20, 0], ammo=[10,10,100,100]),
                        Weapon.Weapon(self.app, self.state, self, bullets_per_second=1, bullets_per_time=1,
                                      spread = [0, 0, 0, 0, 0], damage=100, ammo=[1, 1, 10, 10], bullet_type="exp")]

        self.selected_weapon = 0

        self.health = [100, 100] # 0 текущее хп, 1 макс хп
        self.grenades = [3, 3] # 0 текущее, 1 макс
        self.grenade_pressed = False


        pg.font.init()
        self.font = pg.font.SysFont("sans", 24)

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x,
                                self.y,
                                self.state.map.block_size[0] * 0.8,
                                self.state.map.block_size[1] * 1.6)

        self.weapon_op()
        self.grenade_op()
        self.jump_cooldown[0] -= self.app.clock.get_time() / 1000
        self.movement()
        [w.update() for w in self.weapons]

    def render(self):
        pg.draw.rect(self.app.screen, (255, 255, 255), self.rect)
        self.weapons[self.selected_weapon].render()

        # Прицел & Курсор
        mouse = pg.mouse.get_pos()
        d = ((mouse[0] - self.weapons[self.selected_weapon].rect.right) ** 2 +
             (mouse[1] - self.weapons[self.selected_weapon].rect.centery) ** 2) ** 0.5
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

        # Jump
        if buttons[pg.K_SPACE] and self.jump_fuel[0] > 0:
            self.on_ground = False
            self.jump_fuel[0] -= self.jump_fuel[1] * dt
            self.vel = (self.vel[0], self.vel[1] - self.speed[1] * dt)

        if self.on_ground:
            self.jump_fuel[0] += self.jump_fuel[1] * dt

        self.jump_fuel[0] = min(max(self.jump_fuel[0], 0), self.jump_fuel[3])


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

    def weapon_op(self):
        buttons = pg.key.get_pressed()
        events = self.app.events

        self.weapons[self.selected_weapon].selected = False

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
        self.x, self.y = pos