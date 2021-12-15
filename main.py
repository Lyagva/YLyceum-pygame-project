import pygame as pg
from menu import Menu


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.screen_size = self.screen.get_size()

        self.clock = pg.time.Clock()
        self.fps = 120

        self.running = 'menu'
        self.runner = {'menu': Menu(self)}

    def run(self):
        while self.running:
            self.runner[self.running].run()
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()
