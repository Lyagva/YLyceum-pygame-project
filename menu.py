import pygame as pg


class Button:
    def __init__(self, app, rect_btn, color_btn, text, color_text, size_text, font_text, rect_btn_pushed,
                 color_btn_pushed, text_pushed, color_text_pushed, size_text_pushed, font_text_pushed):
        self.app = app

        self.is_click = False

        #  stats button NO CLICKED
        self.rect_btn, self.color_btn = rect_btn, color_btn  # button
        self.text, self.color_text, self.size_text, self.font_text = text, color_text, size_text, font_text  # text button

        #  stats button CLICKED
        self.rect_btn_pushed, self.color_btn_pushed = rect_btn_pushed, color_btn_pushed  # button
        self.text_pushed, self.color_text_pushed, self.size_text_push, self.font_text_pushed = text_pushed, color_text_pushed, size_text_pushed, font_text_pushed  # text button

    def draw_text(self, surf, text, size, x, y, color, font_name):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect_btn.collidepoint(event.pos):
                    self.is_click = True
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.is_click:
                    pass  # делаем действие
                self.is_click = False

    def render(self):
        if not self.is_click:
            pg.draw.rect(self.app.screen, self.color_btn, self.rect_btn)
            self.draw_text(self.app.screen, self.text, self.size_text, self.rect_btn.x + (self.rect_btn.right - self.rect_btn.x) / 2, self.rect_btn.y + (self.rect_btn.bottom - self.rect_btn.y) // 2, self.color_text, self.font_text)
        elif self.is_click:
            pg.draw.rect(self.app.screen, self.color_btn_pushed, self.rect_btn_pushed)
            self.draw_text(self.app.screen, self.text_pushed, self.size_text_push, self.rect_btn_pushed.x + (self.rect_btn_pushed.right - self.rect_btn_pushed.x) / 2, self.rect_btn_pushed.y + (self.rect_btn_pushed.bottom - self.rect_btn_pushed.y) // 2, self.color_text_pushed, self.font_text_pushed)


class Menu:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button(self.app, pg.Rect(self.app.screen_size[0] / 2 - 75, self.app.screen_size[1] / 2 - 25, 150, 25),
                   pg.Color('red'),
                   'Start', pg.Color('white'), 25, pg.font.match_font('arial'),
                   pg.Rect(self.app.screen_size[0] / 2 - 85, self.app.screen_size[1] / 2 - 35, 170, 60),
                   pg.Color('Blue'),
                   'Start', pg.Color('white'), 35, pg.font.match_font('arial'))
        ]

    def run(self):
        while self.app.running == 'menu':
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.app.running = ''

            for button in self.buttons:
                button.update(events)

            self.app.screen.fill(pg.Color('black'))
            for button in self.buttons:
                button.render()
            pg.display.flip()

            self.app.clock.tick(self.app.fps)
