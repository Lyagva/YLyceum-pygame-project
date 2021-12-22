# Спавн игрока

import pygame as pg


class PlayerSpawn(pg.sprite.Sprite):
    def __init__(self, app, state, pos):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.pos = pos
        self.type = "playerspawn"
        self.rect = pg.Rect(-10000, -10000, 0, 0)

    def update(self):
        self.state.player.set_pos(self.pos)
        self.state.map.delete(self)

    def render(self):
        pass

    def move(self, delta_pos):
        pass