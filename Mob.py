import math

import pygame as pg
import Weapon



def lineRectIntersectionPoints(line, sprites):
    def linesAreParallel(x1, y1, x2, y2, x3, y3, x4, y4):
        return ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)) == 0

    def intersectionPoint(x1, y1, x2, y2, x3, y3, x4, y4):
        Px = ((((x1 * y2) - (y1 * x2)) * (x3 - x4)) - ((x1 - x2) * ((x3 * y4) - (y3 * x4)))) / (
                    ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
        Py = ((((x1 * y2) - (y1 * x2)) * (y3 - y4)) - ((y1 - y2) * ((x3 * y4) - (y3 * x4)))) / (
                    ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
        return Px, Py

    result = []
    for sprite in sprites:
        #  Begin the intersection tests
        result = []
        line_x1, line_y1, line_x2, line_y2 = line[0][0], line[0][1], line[1][0], line[1][1]
        pos_x, pos_y, width, height = sprite.rect

        #  Convert the rectangle into 4 lines
        rect_lines = [(pos_x, pos_y, pos_x + width, pos_y), (pos_x, pos_y + height, pos_x + width, pos_y + height),
                      # top & bottom
                      (pos_x, pos_y, pos_x, pos_y + height),
                      (pos_x + width, pos_y, pos_x + width, pos_y + height)]  # left & right

        #  intersect each rect-side with the line
        for r in rect_lines:
            rx1, ry1, rx2, ry2 = r
            if not linesAreParallel(line_x1, line_y1, line_x2, line_y2, rx1, ry1, rx2, ry2):  # если не парралельны
                pX, pY = intersectionPoint(line_x1, line_y1, line_x2, line_y2, rx1, ry1, rx2, ry2)
                pX = round(pX)
                pY = round(pY)
                # Lines intersect, but is on the rectangle, and between the line end-points?
                if sprite.rect.collidepoint(pX, pY) and min(line_x1, line_x2) <= pX <= max(line_x1, line_x2) and \
                        min(line_y1, line_y2) <= pY <= max(line_y1, line_y2):
                    result.append((pX, pY))  # keep it
                    if len(result) == 2:
                        break  # Once we've found 2 intersection points, that's it
        if result:
            break
    return result


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

        self.weapons = [Weapon.Weapon(self.app, self.main_gameplay, self, ammo=[500, 500, 20000, 20000], bullet_type="exp")]
        self.selected_weapon = 0

        self.gravity = 10
        self.speed = (100, 20)
        self.vel = (0, 0)  # x, y
        self.on_ground = False

        self.visible = 600  # расстояние видимости
        # Recasting
        self.line_to_player = [[self.rect.center, self.main_gameplay.player.rect.center], []]  # координаты и точки пересечения

        self.max_time_jump = self.app.FPS / 5  # 1/5 секунда
        self.time_of_jump = 0
        self.go_to_left, self.go_to_right, self.go_jump = False, False, False

    def update(self):
        if self.rect is None or self.rect.width == 0 or self.rect.height == 0:
            self.rect = pg.Rect(self.x, self.y,
                                self.main_gameplay.map.block_size[0] * 0.8,
                                self.main_gameplay.map.block_size[1] * 1.6)
        # update Recasting
        self.line_to_player = [[self.rect.center, self.main_gameplay.player.rect.center],
                               lineRectIntersectionPoints(self.line_to_player[0], [obg
                                                                                   for lst in self.main_gameplay.map.map
                                                                                   for obg in lst if obg is not None])]

        vector = math.sqrt((self.line_to_player[0][0][0] - self.line_to_player[0][1][0]) ** 2 + (self.line_to_player[0][0][1] - self.line_to_player[0][1][1]) ** 2)
        if self.line_to_player[1] or vector > self.visible:
            self.image.fill(pg.Color('green'))
        else:
            self.image.fill(pg.Color('red'))

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
        self.rect.y += self.vel[1]
        self.wall_collision(0, self.vel[1])

    def render(self):
        self.app.screen.blit(self.image, (self.rect.x, self.rect.y))

        pg.draw.circle(self.app.screen, pg.Color('red'), self.rect.center, self.visible, 4)

        # raycast
        pg.draw.line(self.app.screen, (255, 255, 255), self.line_to_player[0][0], self.line_to_player[0][1], 1)
        for point in self.line_to_player[1]:
            pg.draw.circle(self.app.screen, (255, 255, 255), point, 4)

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

