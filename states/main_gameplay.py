# Это класс состояния игры.

import pygame as pg

import Map
import Player
import Camera


class Update_cam_rect:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 1, 1)


class MainGameplay:
    def __init__(self, app):
        self.app = app

        # GROUPS
        self.bullets = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.grenades = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        # PLAYER
        self.player = Player.Player(self.app, self, (200, 100))

        # MAP
        self.map = Map.Map(self.app, self)

        # Camera
        self.camera = Camera.Camera(self.app, self)

        self.mouse_visible = False

    def update(self):
        pg.mouse.set_visible(self.mouse_visible)

        self.map.update()
        # self.map.map_move((50 * self.app.clock.get_time() / 1000, 0)) # Движение карты. Тест

        # Items
        for item in self.items:
            item.update()

        self.player.update()

        for item in self.mobs:
            item.update()
        for item in self.bullets:
            item.update()
        for item in self.grenades:
            item.update()
        for item in self.explosions:
            item.update()

        applyrect = Update_cam_rect(self.player.rect.centerx - (self.player.rect.centerx - pg.mouse.get_pos()[0]) // 2,
                                    self.player.rect.centery - (self.player.rect.centery - pg.mouse.get_pos()[1]) // 2)

        self.camera.update(applyrect)

        self.camera.mega_apply(applyrect)

    def render(self):
        # Map
        self.map.render()

        # Items
        for item in self.items:
            item.render()

        # Player
        self.player.render()

        for item in self.mobs:
            item.render()
        for item in self.bullets:
            item.render()
        for item in self.grenades:
            item.render()
        for item in self.explosions:
            item.render()
