import pygame as pg

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
                   'New Game', pg.Color('white'), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   'New Game', pg.Color('white'), 25, pg.font.match_font('arial'),
                   [(rewrite_state_to_val, 2)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.5 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.45,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Settings', pg.Color('white'), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   'Settings', pg.Color('white'), 25, pg.font.match_font('arial'),
                   [(rewrite_state_to_val, 3)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                     self.app.screen_size[1] * 0.6 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.45,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Quit', pg.Color('white'), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   'Quit', pg.Color('white'), 25, pg.font.match_font('arial'),
                   [(rewrite_state_to_val, 0)]),

            Button(self.app, pg.Rect(self.app.screen_size[0] * 0.8,
                                     self.app.screen_size[1] * 0.95 - self.app.screen_size[1] * 0.05 / 2,

                                     self.app.screen_size[0] * 0.175,
                                     self.app.screen_size[1] * 0.05),

                   (255, 0, 0),
                   'Credits', pg.Color('white'), 25, pg.font.match_font('arial'),
                   (128, 0, 0),
                   'Credits', pg.Color('white'), 25, pg.font.match_font('arial'),
                   [(rewrite_state_to_val, 4)])
        ]

    def update(self):
        for button in self.buttons:
            button.update(self.app.events)

    def render(self):
        for button in self.buttons:
            button.render()

