import pygame as pg
from button import Button


def rewrite_state_to_val(app, val):
    app.state = val


def rewrite_lvl_to_val(app, val):
    app.states[5].map.file = f'maps/{val}.map'  # Файлик
    app.states[5].map.read_file()


class Levels:
    def __init__(self, app):
        self.app = app

        self.count_levels = 15
        self.location = 'x'  # по какой оси первостепенно распологаются кнопки
        first_pos_x, first_pos_y = 50, 50
        x, y = first_pos_x, first_pos_y
        width, height = 150, 50
        width_push, height_push = 160, 60
        gap_x, gap_y = 50, 50

        stats_buttons = [{'color': pg.Color('DarkRed'),
                         'text': f'Lvl{i + 1}',
                         'color_text': pg.Color('white'),
                         'size_text': 25,
                         'font_text': pg.font.match_font('arial'),
                         'color_push': pg.Color('Red'),
                         'color_text_push': pg.Color('white'),
                         'size_text_push': 35,
                         'change_vars': [(rewrite_state_to_val, 5), (rewrite_lvl_to_val, i + 1)]
                         } for i in range(self.count_levels)]

        self.buttons = [Button(self.app, pg.Rect(self.app.screen_size[0] * 0.025,
                                self.app.screen_size[1] * 0.95 - self.app.screen_size[1] * 0.05 / 2,

                                self.app.screen_size[0] * 0.1,
                                self.app.screen_size[1] * 0.05),

                                (255, 0, 0),
                                'Back', (255, 255, 255), 25, pg.font.match_font('arial'),
                                (128, 0, 0),
                                (255, 255, 255), 25,
                                [(rewrite_state_to_val, 1)]),]
        for i in range(self.count_levels):
            if self.location == 'x':
                if self.app.screen_size[0] - x < width_push:
                    x = first_pos_x
                    y += height + gap_y
                if self.app.screen_size[1] - y < height_push:
                    pass  # перевызов функции с меньшими значениями x y
            elif self.location == 'y':
                if self.app.screen_size[1] - y < height_push:
                    y = first_pos_y
                    x += width + gap_x
                if self.app.screen_size[0] - x < width_push:
                    pass  # перевызов функции с меньшими значениями x y
            self.buttons.append(
                Button(self.app,
                       pg.Rect(x, y, width, height),
                       stats_buttons[i]['color'],
                       stats_buttons[i]['text'], stats_buttons[i]['color_text'], stats_buttons[i]['size_text'], stats_buttons[i]['font_text'],
                       stats_buttons[i]['color_push'],
                       stats_buttons[i]['color_text_push'], stats_buttons[i]['size_text_push'],
                       stats_buttons[i]['change_vars'])
            )
            if self.location == 'x':
                x += width + gap_x
            elif self.location == 'y':
                y += height + gap_y

    def update(self):
        for button in self.buttons:
            button.update(self.app.events)

    def render(self):
        for button in self.buttons:
            button.render()
