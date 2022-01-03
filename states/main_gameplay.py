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
        self.stairs = pg.sprite.Group()


        # PLAYER
        self.player = Player.Player(self.app, self, (200, 100))

        # MAP
        self.map = Map.Map(self.app, self)

        # Camera
        self.camera = Camera.Camera(self.app, self)

        self.mouse_visible = False

    def update(self):
        self.player.update()

        if not self.player.bag_open:
            pg.mouse.set_visible(self.mouse_visible)

            for event in self.app.events:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.mouse.set_visible(True)
                    self.app.state = 2

            self.map.update()
            # self.map.map_move((50 * self.app.clock.get_time() / 1000, 0)) # Движение карты. Тест

            # Items
            for item in self.items:
                item.update()

            for item in self.mobs:
                item.update()
            for item in self.bullets:
                item.update()
            for item in self.grenades:
                item.update()
            for item in self.explosions:
                item.update()
            for item in self.stairs:
                item.update()

            applyrect = Update_cam_rect(self.player.rect.centerx - (self.player.rect.centerx - pg.mouse.get_pos()[0]) // 2,
                                        self.player.rect.centery - (self.player.rect.centery - pg.mouse.get_pos()[1]) // 2)

            self.camera.update(applyrect)

            self.camera.mega_apply(applyrect)

    def render(self):
        # Map
        self.map.render()

        for item in self.stairs:
            item.render()

        # Items
        for item in self.items:
            item.render()

        for item in self.mobs:
            item.render()
        for item in self.bullets:
            item.render()
        for item in self.grenades:
            item.render()
        for item in self.explosions:
            item.render()

        # Player
        self.player.render()

