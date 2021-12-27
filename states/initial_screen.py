import pygame as pg


class InitialScreen:
    def __init__(self, app):
        self.app = app

        self.max_n = self.app.FPS * 2  # 2 сек
        self.n = 0

        self.font = pg.font.SysFont('Comic Sans MS', 60)
        self.textsurface = self.font.render('Lambda-13', False, (0, 0, 0))
        self.text_rect = self.textsurface.get_rect()

    def update(self):
        self.n += 1

        if self.n == self.max_n:
            self.app.state = 1
        else:
            self.textsurface = self.font.render('Lambda-13', False, (self.n % 255, self.n % 255, self.n % 255))

    def render(self):
        self.app.screen.fill(pg.Color('black'))
        self.app.screen.blit(self.textsurface, (self.app.screen_size[0] // 2 - self.text_rect.width // 2,
                                                self.app.screen_size[1] // 2 - self.text_rect.height // 2))
