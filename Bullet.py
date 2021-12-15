# Класс пули. Пуля

# Импорт библиотек
import math
import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, app, main_gameplay):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.x, self.y = main_gameplay.player.rect.center
        self.main_gameplay = main_gameplay
        self.size = 10, 10

        self.pos = (self.x, self.y)

        self.rect = pg.Rect(self.x,
                            self.y,
                            self.size[0],
                            self.size[1])

        self.speed = 10

        mouse_x, mouse_y = pg.mouse.get_pos()

        distance_x = mouse_x - self.x
        distance_y = mouse_y - self.y

        angle = math.atan2(distance_y, distance_x)

        self.vel = (self.speed * math.cos(angle), self.speed * math.sin(angle))

    def update(self):
        self.movement()
        self.wall_collision()

    def render(self):
        pg.draw.rect(self.app.screen, (255, 255, 255), self.rect)

    def movement(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def wall_collision(self):
        map = self.main_gameplay.map.return_map()

        for y in range(self.main_gameplay.map.map_size[1]):
            for x in range(self.main_gameplay.map.map_size[0]):
                other = map[y][x]

                if other:
                    if pg.sprite.collide_rect(self, other):
                        self.kill()