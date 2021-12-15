# Класс игрока. Движение, прицеливание, стрельба и т.д. будут тут.

# Импорт библиотек
import pygame as pg

# Импорт классов
import Bullet

class Player(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay, pos):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.x, self.y = pos
        self.main_gameplay = main_gameplay

        self.speed = (500, 5) # Скорость и сила прыжка
        self.gravity = 10
        self.vel = (0, 0) # Смещение за один кадр

        self.rect = pg.Rect(self.x,
                            self.y,
                            self.main_gameplay.map.block_size[0],
                            self.main_gameplay.map.block_size[1])

        # JUMP
        self.on_ground = False
        self.jump_cooldown = [0, 0.5] # Первое - время, которое изменяется. А второе - время к ресету

        # WEAPON
        self.shooted = False

    def update(self):
        self.jump_cooldown[0] -= self.app.clock.get_time() / 1000
        self.movement()
        self.shoot()

    def render(self):
        pg.draw.rect(self.app.screen, (255, 255, 255), self.rect)

    def movement(self):
        buttons = pg.key.get_pressed()
        self.vel = (0, self.vel[1])
        # Right
        if buttons[pg.K_d]:
            self.vel = (self.vel[0] + self.speed[0] * self.app.clock.get_time() / 1000,
                        self.vel[1])
        # Left
        if buttons[pg.K_a]:
            self.vel = (self.vel[0] - self.speed[0] * self.app.clock.get_time() / 1000,
                        self.vel[1])

        # Jump
        if buttons[pg.K_SPACE] and self.on_ground:
            self.vel = (self.vel[0], self.vel[1] - self.speed[1])
            print("Jump!")

            self.jump_cooldown[0] = self.jump_cooldown[1]
            self.on_ground = False


        # Gravity
        self.vel = (self.vel[0], self.vel[1] + self.gravity * self.app.clock.get_time() / 1000)

        # Horizontal coll
        self.rect.x += self.vel[0]
        self.wall_collision(self.vel[0], 0)

        # Vertical coll
        self.rect.y += self.vel[1]
        self.wall_collision(0, self.vel[1])

    def wall_collision(self, speed_x, speed_y):
        map = self.main_gameplay.map.return_map()

        for y in range(self.main_gameplay.map.map_size[1]):
            for x in range(self.main_gameplay.map.map_size[0]):
                other = map[y][x]

                if other:
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
                        else:
                            self.on_ground = False

    def shoot(self):
        if pg.mouse.get_pressed(3)[0] and self.shooted == False:
            self.main_gameplay.bullets.add(Bullet.Bullet(self.app, self.main_gameplay))

            self.shooted = True
        if not pg.mouse.get_pressed(3)[0]:
            self.shooted = False