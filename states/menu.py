import pygame as pg

from button import Button


def revrite_state_to_val(app, val):
    app.state = val


class Menu:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button(self.app, pg.Rect(self.app.screen_size[0] / 2 - 75, self.app.screen_size[1] / 2 - 25, 150, 25),
                   pg.Color('red'),
                   'Start', pg.Color('white'), 25, pg.font.match_font('arial'),
                   pg.Rect(self.app.screen_size[0] / 2 - 85, self.app.screen_size[1] / 2 - 35, 170, 60),
                   pg.Color('Blue'),
                   'Start', pg.Color('white'), 35, pg.font.match_font('arial'),
                   [(revrite_state_to_val, 2)])
        ]

    def update(self):
        for button in self.buttons:
            button.update(self.app.events)

    def render(self):
        for button in self.buttons:
            button.render()

