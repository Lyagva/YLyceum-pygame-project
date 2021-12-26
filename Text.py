import pygame as pg


class Text:
    def __init__(self, app, center, text, text_color, text_size, text_font):
        self.app = app
        pg.font.init()

        self.text, self.text_color, self.text_size, self.text_font = text, text_color, text_size, text_font  # text button
        self.font = pg.font.Font(self.text_font, self.text_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.center = (center[0] - self.text_surface.get_width() / 2,
                            center[1] - self.text_surface.get_height() / 2)

    def update(self, events=None):
        pass

    def render(self):
        self.app.screen.blit(self.text_surface, self.rect)

    def update_pos(self, center):
        self.rect.center = (center[0] - self.text_surface.get_width() / 2,
                            center[1] - self.text_surface.get_height() / 2)


class UpdatingText:
    def __init__(self, app, center, text, text_color, text_size, text_font, editing_text):
        self.app = app
        pg.font.init()

        self.text, self.text_color, self.text_size, self.text_font, self.editing_text = \
            text, text_color, text_size, text_font, editing_text  # text button

        self.font = pg.font.Font(self.text_font, self.text_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.center = (center[0] - self.text_surface.get_width() / 2,
                            center[1] - self.text_surface.get_height() / 2)

    def update(self, events=None):
        self.text_surface = self.font.render(self.text + str(eval(self.editing_text)), True, self.text_color)

    def render(self):
        self.app.screen.blit(self.text_surface, self.rect)

    def update_pos(self, center):
        self.rect.center = (center[0] - self.text_surface.get_width() / 2,
                            center[1] - self.text_surface.get_height() / 2)