import pygame as pg

from button import Button


def use_heal(app, val):
    print('use', val)
    app.states[5].player.health[0] += val


class Board:
    def __init__(self, app, width, height, left, top, cell_size):
        self.app = app

        self.width = width
        self.height = height
        self.board = [[[] for __ in range(self.width)] for _ in range(self.height)]

        self.board[0][0] = ['medkit10', 10, 5, None]  # название значение количество картинка
        self.buttons = []

        self.left = left
        self.top = top
        self.cell_size = cell_size

        self.rect_board = pg.Rect(0, self.top - 50, self.width * self.cell_size + 50, self.height * self.cell_size + 100)

    def render(self):
        pg.draw.rect(self.app.player.app.screen, pg.Color('brown'), self.rect_board)
        for col in range(self.height):
            for row in range(self.width):
                if not self.board[col][row]:
                    pg.draw.rect(self.app.player.app.screen, pg.Color("white"), (row * self.cell_size + self.left, col * self.cell_size + self.top, self.cell_size, self.cell_size), 1)
                elif self.board[col][row][-1]:
                    self.app.player.app.screen.blit(pg.transform.scale(pg.image.load(self.board[col][row][-1]).convert(),
                                                   (self.cell_size, self.cell_size)),
                                (row * self.cell_size + self.left, col * self.cell_size + self.top))

        for button in self.buttons:
            button.render()

    def get_cell(self, mouse_pos):
        x_click, y_click = mouse_pos
        x_cell = (x_click - self.left) // self.cell_size
        y_cell = (y_click - self.top) // self.cell_size
        if x_cell < 0 or x_cell >= self.width or y_cell < 0 or y_cell >= self.height:
            return None
        return y_cell, x_cell

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        if self.board[cell[0]][cell[1]]:
            val_to_ch = []
            if self.board[cell[0]][cell[1]][0] == 'medkit10':
                val_to_ch = [(use_heal, self.board[cell[0]][cell[1]][1])]

            self.buttons = [Button(self.app.player.app,
                                   pg.Rect(self.left + self.cell_size * cell[0] + 10, self.top + self.cell_size * (cell[0] + 1) + 10, 80, 25),
                                   pg.Color('DarkRed'), 'use', pg.Color('white'), 20, pg.font.get_default_font(),
                                   pg.Color('red'), pg.Color('white'), 22, val_to_ch)]
        else:
            self.buttons = []


class Bag:
    def __init__(self, player, args=None):
        self.player = player
        self.max_capacity = 100  # вместимость макс
        self.board = Board(self, 5, 10, 0, 150, 30)

        if args is None:
            self.items = {
                'medkit': {
                    'dhp10': {'dhp': 10, 'count': 0, 'image': None, 'weight': 5},
                    'dhp20': {'dhp': 20, 'count': 0, 'image': None, 'weight': 10}
                },
                'ammo': {'count': 0, 'image': None, 'weight': 0.05},
                'grenade': {'count': 0, 'image': None, 'weight': 3}
            }
        else:
            self.items = args

        self.capacity = self.items['medkit']['dhp10']['weight'] * self.items['medkit']['dhp10']['count'] + \
                        self.items['medkit']['dhp20']['weight'] * self.items['medkit']['dhp20']['count'] + \
                        self.items['ammo']['weight'] * self.items['ammo']['count'] + \
                        self.items['grenade']['weight'] * self.items['grenade']['count']

    def update(self):
        for button in self.board.buttons:
            button.update(self.player.app.events)

        if not any(list(filter(lambda btn: btn.is_click, self.board.buttons))):
            for event in self.player.app.events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.board.get_click(event.pos)

        if self.board.rect_board.collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)

    def render(self):
        self.board.render()
