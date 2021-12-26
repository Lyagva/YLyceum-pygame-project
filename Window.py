import pygame as pg


class Window:
    def __init__(self, app, state, size, buttons, texts):
        self.app = app
        self.state = state
        self.size = (self.app.screen_size[0] * size[0], self.app.screen_size[1] * size[1])
        self.buttons = buttons
        for item in self.buttons:
            if item.rect.x < self.app.screen_size[0] / 2:
                item.rect.x += self.app.screen_size[0] / 2 - self.size[0] / 2
            else:
                item.rect.x -= self.app.screen_size[0] / 2 - self.size[0] / 2

            if item.rect.y < self.app.screen_size[1] / 2:
                item.rect.y += self.app.screen_size[1] / 2 - self.size[1] / 2
            else:
                item.rect.y -= self.app.screen_size[1] / 2 - self.size[1] / 2

        self.texts = texts
        for item in self.texts:
            if item.rect.x < self.app.screen_size[0] / 2:
                item.rect.x += self.size[0] / 2
            else:
                item.rect.x -= self.size[0] / 2

            if item.rect.y < self.app.screen_size[1] / 2:
                item.rect.y += self.size[1] / 2
            else:
                item.rect.y -= self.size[1] / 2

        self.show = False

    def update(self):
        if self.show:
            for item in self.buttons:
                item.update(self.app.events)
            for item in self.texts:
                item.update()

    def render(self):
        if self.show:
            pg.draw.rect(self.app.screen, (32, 32, 32), pg.Rect(self.app.screen_size[0] / 2 - self.size[0] / 2,
                                                                self.app.screen_size[1] / 2 - self.size[1] / 2,
                                                                int(self.size[0]), int(self.size[1])))

            for button in self.buttons:
                button.render()
            for item in self.texts:
                item.render()
