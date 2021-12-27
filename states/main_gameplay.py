# Это класс состояния игры.

import pygame as pg

import Map
import Player
import Camera
import Window
from Text import Text, UpdatingText
from button import Button


class UpdateCamRect:
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

        self.windows = [Window.Window(self.app, self, (0.75, 0.75), [
            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.95 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.1,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Close', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], [[self.switch_window, 0]]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.875,
                                     self.app.screen_size[1] * 0.95 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.1,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Confirm', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], [[self.switch_window, 0]]),
        ], [Text(self.app,
                 (self.app.screen_size[0] * 0.5,
                  self.app.screen_size[1] * 0.05),
                 "Bio shop", (255, 255, 255), 36, pg.font.match_font("arial")),
            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.5, self.app.screen_size[1] * 0.95),
                         "Money: ", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "self.app.states[5].player.money")])]

        self.f3 = False

    def update(self):
        print(self.player.rect)
        if pg.key.get_pressed()[pg.K_F3]:
            if not self.f3:
                self.switch_window(0)
            self.f3 = True
        else:
            self.f3 = False

        windowed = False
        for w in self.windows:
            if w.show:
                windowed = True
                w.update()

        if not windowed:
            self.app.show_mouse = False

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

            applyrect = UpdateCamRect(
                self.player.rect.centerx - (self.player.rect.centerx - pg.mouse.get_pos()[0]) // 2,
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

        for w in self.windows:
            if w.show:
                w.render()

    def switch_window(self, window_index):
        self.windows[window_index].show = not self.windows[window_index].show
