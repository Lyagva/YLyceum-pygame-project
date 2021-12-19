# Это класс состояния игры.

import pygame as pg

import Map
import Player


class MainGameplay:
    def __init__(self, app):
        self.app = app

        # PLAYER
        self.player = Player.Player(self.app, self, (200, 100))

        # MAP
        self.map = Map.Map(self.app, self)

        # BULLETS
        self.bullets = pg.sprite.Group()
        self.explosions = pg.sprite.Group()

        self.mouse_visible = False

    def update(self):
        pg.mouse.set_visible(self.mouse_visible)

        self.map.update()
        # self.map.map_move((50 * self.app.clock.get_time() / 1000, 0)) # Движение карты. Тест
        self.player.update()

        for item in self.bullets:
            item.update()
        for item in self.explosions:
            item.update()

    def render(self):
        # Map
        self.map.render()

        # Player
        self.player.render()

        for item in self.bullets:
            item.render()
        for item in self.explosions:
            item.render()