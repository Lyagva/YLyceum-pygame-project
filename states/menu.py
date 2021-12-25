from pprint import pprint

import pygame as pg

import Weapon
from button import Button


def rewrite_state_to_val(app, val):
    app.state = val


class Menu:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.4 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.45,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'New Game', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [(rewrite_state_to_val, 2)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.5 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.45,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Settings', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [(rewrite_state_to_val, 3)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.6 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.45,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Quit', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [(rewrite_state_to_val, 0)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.8,
                                     self.app.screen_size[1] * 0.92,

                                     self.app.screen_size[0] * 0.18,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Credits', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   [(rewrite_state_to_val, 4)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.7 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.20,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Save', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   actions_funcs=[self.save]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.275,
                                     self.app.screen_size[1] * 0.7 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.20,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Load', (255, 255, 255), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   (255, 255, 255), 25,
                   actions_funcs=[self.load])
        ]

        self.save_file = "saves/1.txt"

    def update(self):
        for button in self.buttons:
            button.update(self.app.events)

    def render(self):
        for button in self.buttons:
            button.render()

    def save(self):
        with open(self.save_file, mode="w+") as file:
            file.seek(0)
            print(self.app.states[5].player.get_save_data(), file=file)

        print("SAVED")

    def load(self):
        with open(self.save_file, mode="r+") as file:
            data = file.readline()
            data = eval(data)
            print(type(data), data)
            player = self.app.states[5].player
            player.health = data[0]
            player.grenades = data[1]

            player.weapons = [Weapon.Weapon(self.app, self.app.states[5],
                                                               self.app.states[5].player) for _ in range(len(data[2]))]
            for i in range(len(data[2])):
                weapon = player.weapons[i]
                weapon.bullets_per_second = data[2][i][0]
                weapon.damage = data[2][i][1]
                weapon.speed = data[2][i][2]
                weapon.bullets_per_time = data[2][i][3]
                weapon.distance = data[2][i][4]
                weapon.spread = data[2][i][5]
                weapon.ammo = data[2][i][6]
                weapon.reload_time[1] = data[2][i][7]
                weapon.bullet_type = data[2][i][8]
                weapon.image_path = data[2][i][9]
                weapon.shot_type = data[2][i][10]
                weapon.source = data[2][i][11]

            print("LOADED")
