import pygame as pg
from button import Button


class Menu:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button(self.app, pg.Rect(self.app.vars['screen_size'][0] / 2 - 75, self.app.vars['screen_size'][1] / 2 - 25, 150, 25),
                   pg.Color('red'),
                   'Start', pg.Color('white'), 25, pg.font.match_font('arial'),
                   pg.Rect(self.app.vars['screen_size'][0] / 2 - 85, self.app.vars['screen_size'][1] / 2 - 35, 170, 60),
                   pg.Color('Blue'),
                   'Start', pg.Color('white'), 35, pg.font.match_font('arial'),
                   {'running': 'levels'})
        ]

    def run(self):
        while self.app.vars['running'] == 'menu':
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.app.vars['running'] = ''
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.app.vars['running'] = ''

            for button in self.buttons:
                button.update(events)

            self.app.screen.fill(pg.Color('black'))
            for button in self.buttons:
                button.render()
            pg.display.flip()

            self.app.clock.tick(self.app.vars['fps'])
