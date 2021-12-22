# Взрыв

import pygame as pg

class Explosion(pg.sprite.Sprite):
    def __init__(self, app, state, pos, damage):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.pos = pos
        self.damage = damage

        self.radius = [0, 1000, 100]  # 0 текущий, 1 дельта, 2 макс
        self.rect = pg.Rect(self.pos[0] - self.radius[2] / 2, self.pos[1] - self.radius[2] / 2, self.radius[2], self.radius[2])

        # Map collide & dmg
        map = self.state.map.return_map()
        for row in range(len(map)):
            for col in range(len(map[row])):
                other = map[row][col]
                if other:
                    if other.type not in ["block", "jumppad", "playerspawn"] and pg.sprite.collide_rect(self, other):
                        other.get_damage(self.damage)

        # Player collide & dmg
        if pg.sprite.collide_rect(self, self.state.player):
            self.state.player.get_damage(self.damage)


    def render(self):
        pg.draw.circle(self.app.screen, (255, 0, 0), self.pos, self.radius[0])
        # pg.draw.rect(self.app.screen, (0, 255, 0), self.rect)

    def update(self):
        self.radius[0] += self.radius[1] * self.app.clock.get_time() / 1000
        if self.radius[0] >= self.radius[2]:
            self.kill()

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]