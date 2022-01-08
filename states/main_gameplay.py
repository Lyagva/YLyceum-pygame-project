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
        self.stairs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()

        # PLAYER
        self.stats = {"kills": 0, "time": 0}
        self.player = Player.Player(self.app, self)

        # MAP
        self.maps_list = []
        self.current_mission = 0
        self.current_sector = -1
        self.read_map_list()

        self.map = Map.Map(self.app, self)
        self.map.file = "maps/Hub.map"
        self.map.read_file()

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
                                   [], ["self.app.states[5].switch_window(2)"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.825,
                                                     self.app.screen_size[1] * 0.95 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.15,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Start Mission', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].switch_window(2)",
                                        "self.app.states[5].teleport_to_next_sector()"])],
                                      [Text(self.app,
                                            (self.app.screen_size[
                                                 0] * 0.5,
                                             self.app.screen_size[
                                                 1] * 0.05),
                                            "Mission Teleport",
                                            (255, 255, 255), 36,
                                            pg.font.match_font(
                                                "arial")),

                                       UpdatingText(self.app,
                                                    (
                                                        self.app.screen_size[
                                                            0] * 0.625,
                                                        self.app.screen_size[
                                                            1] * 0.95),
                                                    "", (
                                                        255, 255, 255),
                                                    25,
                                                    pg.font.match_font(
                                                        "arial"),
                                                    "'Progress:    ' + str(int((self.app.states[5].current_mission + 1) / "
                                                    "len(self.app.states[5].maps_list) * 100)) + '%'"),

                                       UpdatingText(self.app,
                                                    (
                                                        self.app.screen_size[
                                                            0] * 0.05,
                                                        self.app.screen_size[
                                                            1] * 0.15),
                                                    "", (
                                                        255, 255, 255),
                                                    25,
                                                    pg.font.match_font(
                                                        "arial"),
                                                    "'Name:    ' + str(self.app.states[5]."
                                                    "maps_list[self.app.states[5].current_mission][0])",
                                                    align="topleft"),

                                       UpdatingText(self.app,
                                                    (
                                                        self.app.screen_size[
                                                            0] * 0.05,
                                                        self.app.screen_size[
                                                            1] * 0.25),
                                                    "", (
                                                        255, 255, 255),
                                                    25,
                                                    pg.font.match_font(
                                                        "arial"),
                                                    "'Length:    ' + str(len(self.app.states[5]."
                                                    "maps_list[self.app.states[5].current_mission][1])) + '  Sectors'",
                                                    align="topleft"),
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
                                   [], ["self.app.states[5].switch_window(3)"]),

                            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.825,
                                                     self.app.screen_size[1] * 0.95 - self.app.screen_size[
                                                         1] * 0.05 / 2,

                                                     self.app.screen_size[0] * 0.15,
                                                     self.app.screen_size[1] * 0.05),

                                   (255, 0, 0),
                                   'Teleport', (255, 255, 255), 25, pg.font.match_font('arial'),
                                   (128, 0, 0),
                                   (255, 255, 255), 25,
                                   [], ["self.app.states[5].switch_window(3)",
                                        "self.app.states[5].teleport_to_next_sector()"])],
                                      [Text(self.app,
                                            (self.app.screen_size[0] * 0.5,
                                             self.app.screen_size[
                                                 1] * 0.05),
                                            "Sector Clear",
                                            (255, 255, 255), 36,
                                            pg.font.match_font("arial")),

                                       UpdatingText(self.app,
                                                    (self.app.screen_size[0] * 0.625, self.app.screen_size[1] * 0.95),
                                                    "", (255, 255, 255), 25,
                                                    pg.font.match_font("arial"),
                                                    "'Progress:    ' + "
                                                    "str(int((self.app.states[5].current_sector + 1) / "
                                                    "len(self.app.states[5]."
                                                    "maps_list[self.app.states[5].current_mission][1]) * 100)) + '%'"),

                                       UpdatingText(self.app,
                                                    (self.app.screen_size[
                                                         0] * 0.05,
                                                     self.app.screen_size[
                                                         1] * 0.15),
                                                    "", (255, 255, 255), 25,
                                                    pg.font.match_font(
                                                        "arial"),
                                                    "'Kills:    ' + str(self.app.states[5].stats['kills'])",
                                                    align="topleft"),

                                       UpdatingText(self.app,
                                                    (self.app.screen_size[
                                                         0] * 0.05,
                                                     self.app.screen_size[
                                                         1] * 0.25),
                                                    "", (255, 255, 255), 25,
                                                    pg.font.match_font(
                                                        "arial"),
                                                    "'Time:    ' + str(self.app.states[5].stats['time'] // 60) + ':' + "
                                                    "str(self.app.states[5].stats['time'] % 60)",
                                                    align="topleft"),
                                       ])
                        ]

        self.f3 = False
        self.f4 = False
        self.f5 = False

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

        if pg.key.get_pressed()[pg.K_F5]:
            if not self.f5:
                self.switch_window(2)
            self.f5 = True
        else:
            self.f5 = False

        windowed = False
        for w in self.windows:
            if w.show:
                windowed = True
                w.update()

        if not windowed:
            self.app.show_mouse = False

            for event in self.app.events:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.mouse.set_visible(True)
                    self.app.state = 2

            self.map.update()

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
            for item in self.npcs:
                item.update()
            self.player.update()

            apply_rect = UpdateCamRect(
                self.player.rect.centerx - (self.player.rect.centerx - pg.mouse.get_pos()[0]) // self.camera.mouse_k,
                self.player.rect.centery - (self.player.rect.centery - pg.mouse.get_pos()[1]) // self.camera.mouse_k)

            self.camera.update(apply_rect)

            self.camera.mega_apply(apply_rect)

    def render(self):
        # Map
        self.map.render()

        for item in self.stairs:
            item.render()

        # Items
        for item in self.npcs:
            item.render()
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

    def read_map_list(self, file_name="maps/map_list.maps"):
        with open(file_name, mode="r") as file:
            map_list = [line.replace("\n", "").split(";") for line in file.readlines()]  # Делим по строчкам и ;
            map_list = [[line[0], line[1].split(",")]
                        for line in map_list]
            map_list = [[line[0], ["maps/" + str(part) for part in line[1]]]
                        for line in map_list]  # Добавляем к картам maps/

            print(map_list)
            self.maps_list = map_list

    def teleport_to_next_sector(self):
        self.current_sector += 1
        if self.current_sector >= len(self.maps_list[self.current_mission][1]):
            self.current_sector = -1
            self.current_mission += 1
            self.map.file = "maps/hub.map"
        else:
            print(self.current_sector, self.current_mission)
            self.map.file = self.maps_list[self.current_mission][1][self.current_sector]

        self.map.read_file()

        # Player
        self.player.render()

