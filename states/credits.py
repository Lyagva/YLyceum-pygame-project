import pygame as pg
from button import Button


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
                                'Back', pg.Color('white'), 25, pg.font.match_font('arial'),
                                (128, 0, 0),
                                'Back', pg.Color('white'), 25, pg.font.match_font('arial'),
                                [(rewrite_state_to_val, 1)]),

                        Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                self.app.screen_size[1] * 0.95 - self.app.screen_size[1] * 0.05 / 2,

                                self.app.screen_size[0] * 0.1,
                                self.app.screen_size[1] * 0.05),

                                (255, 0, 0),
                                'Back', pg.Color('white'), 25, pg.font.match_font('arial'),
                                (128, 0, 0),
                                'Back', pg.Color('white'), 25, pg.font.match_font('arial'),
                                [(rewrite_state_to_val, 1)]),
                        ]

    def update(self):
        for button in self.buttons:
            button.update(self.app.events)

    def render(self):
        for button in self.buttons:
            button.render()
