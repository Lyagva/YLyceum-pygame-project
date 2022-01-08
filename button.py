import pygame as pg

from Text import Text


class Button:
    def __init__(self, app, rect, color, msg, text_color, text_size, text_font,
                 color_pressed, text_color_pressed, text_size_pressed,
                 actions_vars=None, actions_funcs=None):
        self.app = app

        self.is_click = False

        #  stats button NO CLICKED
        self.rect, self.color_btn = rect, color  # button
        self.prev_rect = self.rect.copy()

        #  stats button CLICKED
        self.color_btn_pushed = color_pressed  # button

        self.text = Text(self.app, (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2),
                         msg, text_color, text_size, text_font)
        self.text_pressed = Text(self.app, (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2),
                                 msg, text_color_pressed, text_size_pressed, text_font)

        self.actions_vars = actions_vars
        self.actions_funcs = actions_funcs

    def on_click(self):
        if self.actions_vars:
            for func, val in self.actions_vars:
                func(self.app, val)

        if self.actions_funcs:
            for act in self.actions_funcs:
                exec(act)

    def update(self, events):
        if self.prev_rect != self.rect:
            self.text.rect.x += self.rect.x - self.prev_rect.x
            self.text.rect.y += self.rect.y - self.prev_rect.y

            self.text_pressed.rect.x += self.rect.x - self.prev_rect.x
            self.text_pressed.rect.y += self.rect.y - self.prev_rect.y

            self.prev_rect = self.rect

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_click = True
                    print('click')
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.is_click:
                        self.on_click()
                self.is_click = False

    def render(self):
        if not self.is_click:
            pg.draw.rect(self.app.screen, self.color_btn, self.rect)
            self.text.render()
        elif self.is_click:
            pg.draw.rect(self.app.screen, self.color_btn_pushed, self.rect)
            self.text_pressed.render()
