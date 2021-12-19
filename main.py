import pygame as pg

from menu import Menu
from levels import Levels
from game import Game


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        # no pygame vars
        self.vars = {'screen_size': self.screen.get_size(),
                     'running': 'menu',
                     'fps': 120,
                     'chosen_level': None
                     }

    def run(self):
        self.vars['runner'] = {'menu': Menu(self), 'levels': Levels(self), 'game': Game(self)}

        while self.vars['running']:
            self.vars['runner'][self.vars['running']].run()
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()
