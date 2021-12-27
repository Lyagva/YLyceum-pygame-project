import pygame as pg


class Text:
    def __init__(self, app, pos, text, text_color, text_size, text_font):
        self.app = app
        pg.font.init()

        self.text, self.text_color, self.text_size, self.text_font = text, text_color, text_size, text_font  # text button
        self.font = pg.font.Font(self.text_font, self.text_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.topleft = (pos[0] - self.text_surface.get_width() / 2,
                             pos[1] - self.text_surface.get_height() / 2)

    def update(self, events=None):
        pass

    def render(self):
        self.app.screen.blit(self.text_surface, self.rect)

    def update_center(self, center):
        self.rect.center = (center[0] - self.text_surface.get_width() / 2,
                            center[1] - self.text_surface.get_height() / 2)

    def update_pos(self, pos):
        self.rect.topleft = pos


class UpdatingText:
    def __init__(self, app, pos, text, text_color, text_size, text_font, editing_text):
        self.app = app
        pg.font.init()

        self.text, self.text_color, self.text_size, self.text_font, self.editing_text = \
            text, text_color, text_size, text_font, editing_text  # text button

        self.font = pg.font.Font(self.text_font, self.text_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.topleft = (pos[0] - self.text_surface.get_width() / 2,
                             pos[1] - self.text_surface.get_height() / 2)
        self.prev_offset = (self.text_surface.get_width() / 2, self.text_surface.get_height() / 2)

    def update(self, events=None):
        self.text_surface = self.font.render(self.text + str(eval(self.editing_text)), True, self.text_color)
        self.rect.x -= self.text_surface.get_width() / 2 - self.prev_offset[0]
        self.rect.y -= self.text_surface.get_height() / 2 - self.prev_offset[1]
        self.prev_offset = (self.text_surface.get_width() / 2, self.text_surface.get_height() / 2)

    def render(self):
        self.app.screen.blit(self.text_surface, self.rect)

    def update_center(self, center):
        self.rect.center = (center[0] - self.text_surface.get_width() / 2,
                            center[1] - self.text_surface.get_height() / 2)

    def update_pos(self, pos):
        self.rect.topleft = pos
