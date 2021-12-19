import pygame as pg


class Button:
    def __init__(self, app, rect_btn, color_btn, text, color_text, size_text, font_text, rect_btn_pushed,
                 color_btn_pushed, text_pushed, color_text_pushed, size_text_pushed, font_text_pushed,
                 variable_values_to_change):
        self.app = app

        self.is_click = False

        #  stats button NO CLICKED
        self.rect_btn, self.color_btn = rect_btn, color_btn  # button
        self.text, self.color_text, self.size_text, self.font_text = text, color_text, size_text, font_text  # text button

        #  stats button CLICKED
        self.rect_btn_pushed, self.color_btn_pushed = rect_btn_pushed, color_btn_pushed  # button
        self.text_pushed, self.color_text_pushed, self.size_text_push, self.font_text_pushed = text_pushed, color_text_pushed, size_text_pushed, font_text_pushed  # text button

        # what do if cliked
        self.variable_values_to_change = variable_values_to_change

    def draw_text(self, surf, text, size, x, y, color, font_name):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def on_click(self):
        for funck, val in self.variable_values_to_change:
            funck(self.app, val)

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect_btn.collidepoint(event.pos):
                    self.is_click = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.rect_btn.collidepoint(event.pos):
                    if self.is_click:
                        self.on_click()
                self.is_click = False

    def render(self):
        if not self.is_click:
            pg.draw.rect(self.app.screen, self.color_btn, self.rect_btn)
            self.draw_text(self.app.screen, self.text, self.size_text, self.rect_btn.x + (self.rect_btn.right - self.rect_btn.x) / 2, self.rect_btn.y + (self.rect_btn.bottom - self.rect_btn.y) // 2, self.color_text, self.font_text)
        elif self.is_click:
            pg.draw.rect(self.app.screen, self.color_btn_pushed, self.rect_btn_pushed)
            self.draw_text(self.app.screen, self.text_pushed, self.size_text_push, self.rect_btn_pushed.x + (self.rect_btn_pushed.right - self.rect_btn_pushed.x) / 2, self.rect_btn_pushed.y + (self.rect_btn_pushed.bottom - self.rect_btn_pushed.y) // 2, self.color_text_pushed, self.font_text_pushed)
