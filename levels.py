import pygame as pg
from button import Button


class Levels:
    def __init__(self, app):
        self.app = app

        self.count_levels = 15
        stats_butons = [{'color': pg.Color('DarkRed'),
                         'text': f'Lvl{i + 1}',
                         'color_text': pg.Color('white'),
                         'size_text': 25,
                         'font_text': pg.font.match_font('arial'),
                         'color_push': pg.Color('Red'),
                         'text_push': f'Lvl{i + 1}',
                         'color_text_push': pg.Color('white'),
                         'size_text_push': 35,
                         'font_text_push': pg.font.match_font('arial'),
                         'change_vars': {'running': 'game', 'chosen_level': i + 1}
                         } for i in range(self.count_levels)]
        self.location = 'x'  # по какой оси первостепенно распологаются кнопки
        first_pos_x, first_pos_y = 50, 50
        x, y = first_pos_x, first_pos_y
        width, height = 150, 50
        width_push, height_push = 160, 60
        gap_x, gap_y = 50, 50

        print(self.app.vars['screen_size'])
        self.buttons = []
        for i in range(self.count_levels):
            if self.location == 'x':
                if self.app.vars['screen_size'][0] - x < width_push:
                    x = first_pos_x
                    y += height + gap_y
                if self.app.vars['screen_size'][1] - y < height_push:
                    pass  # перевызов функции с меньшими значениями x y
            elif self.location == 'y':
                if self.app.vars['screen_size'][1] - y < height_push:
                    y = first_pos_y
                    x += width + gap_x
                if self.app.vars['screen_size'][0] - x < width_push:
                    pass  # перевызов функции с меньшими значениями x y
            print(x, y)
            self.buttons.append(
                Button(self.app,
                       pg.Rect(x, y, width, height),
                       stats_butons[i]['color'],
                       stats_butons[i]['text'], stats_butons[i]['color_text'], stats_butons[i]['size_text'], stats_butons[i]['font_text'],
                       pg.Rect(x - (abs(width - width_push) / 2), y - (abs(height - height_push) / 2), width_push, height_push),
                       stats_butons[i]['color_push'],
                       stats_butons[i]['text_push'], stats_butons[i]['color_text_push'], stats_butons[i]['size_text_push'], stats_butons[i]['font_text_push'],
                       stats_butons[i]['change_vars'])
            )
            if self.location == 'x':
                x += width + gap_x
            elif self.location == 'y':
                y += height + gap_y

    def run(self):
        while self.app.vars['running'] == 'levels':
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
