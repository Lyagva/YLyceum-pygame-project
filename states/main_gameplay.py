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
                   [], ["self.app.states[5].switch_window(0)"]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.15 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Health', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], ["self.app.states[5].player.make_upgrade('Health')"]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.25 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Max grenades', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], ["self.app.states[5].player.make_upgrade('Grenades Count')"]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.35 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Speed', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], ["self.app.states[5].player.make_upgrade('Speed')"]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.45 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.2,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Jump Fuel', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [], ["self.app.states[5].player.make_upgrade('Jump Fuel')"]),

        ], [Text(self.app,
                 (self.app.screen_size[0] * 0.5,
                  self.app.screen_size[1] * 0.05),
                 "Upgrades Shop", (255, 255, 255), 36, pg.font.match_font("arial")),
            UpdatingText(self.app,
                         (self.app.screen_size[0] * 0.625, self.app.screen_size[1] * 0.95),
                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                         "str(self.app.states[5].player.money) + '$'"),

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
            ]),
                        Window.Window(self.app, self, (0.75, 0.75), [
                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                                     self.app.screen_size[1] * 0.95 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.1,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Close', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].switch_window(1)"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                                     self.app.screen_size[1] * 0.15 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.2,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Optic', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].player.weapons[self.app.states["
                                        "5].player.selected_weapon].upgrade('optic')"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                                     self.app.screen_size[1] * 0.25 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.2,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Muzzle', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].player.weapons[self.app.states["
                                        "5].player.selected_weapon].upgrade('muzzle')"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                                     self.app.screen_size[1] * 0.35 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.2,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Underbarrel', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].player.weapons[self.app.states["
                                        "5].player.selected_weapon].upgrade('underbarrel')"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                                     self.app.screen_size[1] * 0.45 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.2,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Stock', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].player.weapons[self.app.states["
                                        "5].player.selected_weapon].upgrade('stock')"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                                     self.app.screen_size[1] * 0.8 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.2,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Magazine', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].player.weapons[self.app.states["
                                        "5].player.selected_weapon].upgrade('magazine')"]),

                        ], [Text(self.app,
                                 (self.app.screen_size[0] * 0.5,
                                  self.app.screen_size[1] * 0.05),
                                 "Upgrades Shop", (255, 255, 255), 36, pg.font.match_font("arial")),
                            UpdatingText(self.app,
                                         (self.app.screen_size[0] * 0.625, self.app.screen_size[1] * 0.95),
                                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                                         "str(self.app.states[5].player.money) + '$'"),

                            UpdatingText(self.app,
                                         (self.app.screen_size[0] * 0.75,
                                          self.app.screen_size[1] * 0.15),
                                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                                         """"Lvl: " + str(self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["optic"].lvl[0]) + "/" + str(
                                         self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["optic"].lvl[1]) + "    " + self.app.states[
                                         5].player.weapons[self.app.states[5].player.selected_weapon].mods[
                                         "optic"].get_effect()"""),

                            UpdatingText(self.app,
                                         (self.app.screen_size[0] * 0.75,
                                          self.app.screen_size[1] * 0.25),
                                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                                         """"Lvl: " + str(self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["muzzle"].lvl[0]) + "/" + str(
                                         self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["muzzle"].lvl[1]) + "     " + self.app.states[
                                         5].player.weapons[ self.app.states[5].player.selected_weapon].mods[
                                         "muzzle"].get_effect()"""),

                            UpdatingText(self.app,
                                         (self.app.screen_size[0] * 0.75,
                                          self.app.screen_size[1] * 0.35),
                                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                                         """"Lvl: " + str(self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["underbarrel"].lvl[0]) + "/" + str(
                                         self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["underbarrel"].lvl[1]) + "     " + self.app.states[
                                         5].player.weapons[ self.app.states[5].player.selected_weapon].mods[
                                         "underbarrel"].get_effect()"""),

                            UpdatingText(self.app,
                                         (self.app.screen_size[0] * 0.75,
                                          self.app.screen_size[1] * 0.45),
                                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                                         """"Lvl: " + str(self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["stock"].lvl[0]) + "/" + str(
                                         self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["stock"].lvl[1]) + "     " + self.app.states[
                                         5].player.weapons[ self.app.states[5].player.selected_weapon].mods[
                                         "stock"].get_effect()"""),

                            UpdatingText(self.app,
                                         (self.app.screen_size[0] * 0.75,
                                          self.app.screen_size[1] * 0.8),
                                         "", (255, 255, 255), 25, pg.font.match_font("arial"),
                                         """"Lvl: " + str(self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["magazine"].lvl[0]) + "/" + str(
                                         self.app.states[5].player.weapons[self.app.states[ 
                                         5].player.selected_weapon].mods["magazine"].lvl[1]) + "     " + self.app.states[
                                         5].player.weapons[ self.app.states[5].player.selected_weapon].mods[
                                         "magazine"].get_effect()""")
                            ])]

        self.f3 = False
        self.f4 = False

    def update(self):
        if pg.key.get_pressed()[pg.K_F3]:
            if not self.f3:
                self.switch_window(0)
            self.f3 = True
        else:
            self.f3 = False

        if pg.key.get_pressed()[pg.K_F4]:
            if not self.f4:
                self.switch_window(1)
            self.f4 = True
        else:
            self.f4 = False

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

        for w in self.windows:
            if w.show:
                w.render()

    def switch_window(self, window_index):
        self.windows[window_index].show = not self.windows[window_index].show
