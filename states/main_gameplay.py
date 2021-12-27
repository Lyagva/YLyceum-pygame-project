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

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.15 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Health', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], [[self.player.make_upgrade, "Health"]]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.25 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Max grenades', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], [[self.player.make_upgrade, "Grenades Count"]]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.35 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Speed', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], [[self.player.make_upgrade, "Speed"]]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.45 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Jump Fuel', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], [[self.player.make_upgrade, "Jump Fuel"]]),

        ], [Text(self.app,
                 (self.app.screen_size[0] * 0.5,
                  self.app.screen_size[1] * 0.05),
                 "Upgrades Shop", (255, 255, 255), 36, pg.font.match_font("arial")),
            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.5, self.app.screen_size[1] * 0.95),
                         "Money: ", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "self.app.states[5].player.money"),

            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.75,
                          self.app.screen_size[1] * 0.15),
                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "'Lvl: ' + str(self.app.states[5].player.upgrades['Health'][0]) + '/' + "
                         "str(self.app.states[5].player.upgrades['Health'][1]) + '    Cost: ' + "
                         "str(self.app.states[5].player.upgrades['Health'][2]) + '$    Effect: ' + "
                         "str(self.app.states[5].player.upgrades['Health'][4]) + "
                         "str(self.app.states[5].player.upgrades['Health'][3]) + ' hp '"),

            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.75,
                          self.app.screen_size[1] * 0.25),
                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "'Lvl: ' + str(self.app.states[5].player.upgrades['Grenades Count'][0]) + '/' + "
                         "str(self.app.states[5].player.upgrades['Grenades Count'][1]) + '    Cost: ' + "
                         "str(self.app.states[5].player.upgrades['Grenades Count'][2]) + '$    Effect: ' + "
                         "str(self.app.states[5].player.upgrades['Grenades Count'][4]) + "
                         "str(self.app.states[5].player.upgrades['Grenades Count'][3]) + ' grenades '"),

            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.75,
                          self.app.screen_size[1] * 0.35),
                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "'Lvl: ' + str(self.app.states[5].player.upgrades['Speed'][0]) + '/' + "
                         "str(self.app.states[5].player.upgrades['Speed'][1]) + '    Cost: ' + "
                         "str(self.app.states[5].player.upgrades['Speed'][2]) + '$    Effect: ' + "
                         "str(self.app.states[5].player.upgrades['Speed'][4]) + "
                         "str(self.app.states[5].player.upgrades['Speed'][3]) + ' speed '"),

            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.75,
                          self.app.screen_size[1] * 0.45),
                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "'Lvl: ' + str(self.app.states[5].player.upgrades['Jump Fuel'][0]) + '/' + "
                         "str(self.app.states[5].player.upgrades['Jump Fuel'][1]) + '    Cost: ' + "
                         "str(self.app.states[5].player.upgrades['Jump Fuel'][2]) + '$    Effect: ' + "
                         "str(self.app.states[5].player.upgrades['Jump Fuel'][4]) + "
                         "str(self.app.states[5].player.upgrades['Jump Fuel'][3]) + ' fuel '")
            ])]

        self.f3 = False

    def update(self):
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

            apply_rect = UpdateCamRect(
                self.player.rect.centerx - (self.player.rect.centerx - pg.mouse.get_pos()[0]) // self.camera.mouse_k,
                self.player.rect.centery - (self.player.rect.centery - pg.mouse.get_pos()[1]) // self.camera.mouse_k)

            self.camera.update(apply_rect)

            self.camera.mega_apply(apply_rect)

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
