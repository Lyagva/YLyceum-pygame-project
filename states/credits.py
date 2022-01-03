import pygame as pg
from button import Button
from Text import Text


def rewrite_state_to_val(app, val):
    app.state = val


class Credits:
    def __init__(self, app):
        self.app = app

        self.buttons = [Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                self.app.screen_size[1] * 0.95 - self.app.screen_size[1] * 0.05 / 2,

                                self.app.screen_size[0] * 0.1,
                                self.app.screen_size[1] * 0.05),

                                (255, 0, 0),
                                'Back', (255, 255, 255), 25, pg.font.match_font('arial'),
                                (128, 0, 0),
                                (255, 255, 255), 25,
                                [(rewrite_state_to_val, 1)]),
                        ]

        self.texts = [Text(self.app,
                           (self.app.screen_size[0] * 0.5,
                            self.app.screen_size[1] * 0.1),
                           "Main Coder - Lyagva", (255, 255, 255), 25, pg.font.match_font("arial")),
                      Text(self.app,
                           (self.app.screen_size[0] * 0.5,
                            self.app.screen_size[1] * 0.2),
                           "Main Coder - Vova", (255, 255, 255), 25, pg.font.match_font("arial")),
                      Text(self.app,
                           (self.app.screen_size[0] * 0.5,
                            self.app.screen_size[1] * 0.24),
                           "Again?..", (64, 64, 64), 12, pg.font.match_font("arial")),

                      Text(self.app,
                           (self.app.screen_size[0] * 0.5,
                            self.app.screen_size[1] * 0.4),
                           "Music - Lyagva", (255, 255, 255), 25, pg.font.match_font("arial")),
                      Text(self.app,
                           (self.app.screen_size[0] * 0.5,
                            self.app.screen_size[1] * 0.5),
                           "Music - Weltraum", (255, 255, 255), 25, pg.font.match_font("arial"))
                      ]

    def update(self):
        for item in self.buttons:
            item.update(self.app.events)
        for item in self.texts:
            item.update()

    def render(self):
        for button in self.buttons:
            button.render()
        for item in self.texts:
            item.render()