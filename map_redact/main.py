import pygame as pg
import imghdr
import os


class Board:
    # создание поля
    def __init__(self, app, width, height, left, top, cell_size):
        self.app = app

        self.width = width
        self.height = height
        self.board = [[[] for __ in range(self.width)] for _ in range(self.height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for col in range(self.height):
            for row in range(self.width):
                if not self.board[col][row]:
                    pg.draw.rect(screen, pg.Color("white"),
                                 (row * self.cell_size + self.left, col * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)
                else:
                    screen.blit(pg.transform.scale(pg.image.load(self.board[col][row][1]).convert(),
                                                   (self.cell_size, self.cell_size)),
                                (row * self.cell_size + self.left, col * self.cell_size + self.top))

    def get_cell(self, mouse_pos):
        x_click, y_click = mouse_pos
        x_cell = (x_click - self.left) // self.cell_size
        y_cell = (y_click - self.top) // self.cell_size
        if x_cell < 0 or x_cell >= self.width or y_cell < 0 or y_cell >= self.height:
            return None
        return y_cell, x_cell

    def get_click(self, mouse_pos, func):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, func)

    def on_click(self, cell, func):
        print(cell)
        if func == 'set pict':
            if cell:
                parse = self.app.picture.split('\\')
                self.board[int(cell[0])][int(cell[1])] = [parse[-2], f'images/{parse[-2]}/{parse[-1]}', '']
                self.app.params_of_cell = [int(cell[0]), int(cell[1]), '']
        elif func == 'remove pict':
            if cell:
                self.board[int(cell[0])][int(cell[1])] = []
        elif func == 'get_params':
            if cell:
                if self.board[int(cell[0])][int(cell[1])]:
                    self.app.params_of_cell = [int(cell[0]), int(cell[1]), self.board[int(cell[0])][int(cell[1])][2]]
                else:
                    self.app.params_of_cell = None
            else:
                self.app.params_of_cell = None


class Images(Board):
    def __init__(self, app, left, top, cell_size, dir):
        self.app = app
        self.images = []
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if imghdr.what(file_path):
                    self.images.append(file_path)

        self.height = len(self.images)
        self.width = 1

        self.left = left
        self.top = top
        self.cell_size = cell_size

        self.board = [[self.images[i]] for i in range(self.height)]

    def render(self, screen):
        for col in range(self.height):
            for row in range(self.width):
                try:
                    if self.board[col][row]:
                        x, y = row * self.cell_size + self.left, col * self.cell_size + self.top
                        if self.app.screen_rect.collidepoint((x, y)):
                            screen.blit(pg.transform.scale(pg.image.load(self.board[col][row]).convert(), (self.cell_size, self.cell_size)),
                                        (x, y))
                        if self.app.picture == self.board[col][row]:
                            pg.draw.rect(screen, pg.Color('white'), pg.Rect(x, y, self.cell_size, self.cell_size), 2)
                except IndexError:
                    pass

    def on_click(self, cell, unuse):
        self.app.process = 'remove picture'
        self.app.picture = self.board[cell[0]][cell[1]]
        self.app.x_pict, self.app.y_pict, self.app.wid_pict, self.app.height_pict = pg.mouse.get_pos()[0] - self.cell_size // 2, pg.mouse.get_pos()[1] - self.cell_size // 2, self.cell_size // 2, self.cell_size // 2


class Buttons(Board):
    def __init__(self, app, width, height, left, top, cell_size):
        super().__init__(app, width, height, left, top, cell_size)
        self.board = [[['', 'DarkRed'] for __ in range(self.width)] for _ in range(self.height)]
        self.chosen = None

    def draw_text(self, surf, text, size, x, y, color, font_name):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def render(self, screen):
        for col in range(self.height):
            for row in range(self.width):
                pg.draw.rect(screen, self.board[col][row][1],
                             (row * self.cell_size + self.left, col * self.cell_size + self.top, self.cell_size,
                              self.cell_size))
                self.draw_text(screen, self.board[col][row][0], 20,
                               row * self.cell_size + self.left + self.cell_size / 2,
                               col * self.cell_size + self.top + self.cell_size / 2,
                               pg.Color('white'), pg.font.match_font('arial'))
                if self.chosen == self.board[col][row][0]:
                    pg.draw.rect(screen, pg.Color('white'), (row * self.cell_size + self.left, col * self.cell_size + self.top, self.cell_size,
                                                             self.cell_size), 2)

    def on_click(self, cell, unuse):
        print(cell)
        for col in range(self.height):
            for row in range(self.width):
                if (col, row) == cell:
                    if self.board[col][row][1] == 'DarkRed':
                        self.board[col][row][1] = 'red'
                        self.chosen = self.board[col][row][0]
                    else:
                        self.board[col][row][1] = 'DarkRed'
                        self.chosen = None
                else:
                    self.board[col][row][1] = 'DarkRed'


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.screen_size = pg.display.get_window_size()

        self.clock = pg.time.Clock()

        self.screen_rect = pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])

        self.zoom = 2
        self.scrolling = 100
        self.process = None

        self.ctrl_clicked = False

        self.input_rect = pg.Rect(self.screen_size[0] // 2 - 100, 0, 200, 75)
        self.width_of_input_rect = 200
        self.params_of_cell = None

        self.picture = None
        self.x_pict, self.y_pict, self.wid_pict, self.height_pict = None, None, None, None

        self.fps = 120
        self.running = True

    def draw_text(self, surf, text, size, x, y, color, font_name):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def run(self):
        board = Board(self, 50, 50, 100, 100, 20)

        folders = dict()
        for dirpath, dirnames, filenames in os.walk('images'):
            for dir in dirnames:
                folders[dir] = Images(self, 50, 0, 50, os.path.join(dirpath, dir))

        toolboard = Buttons(self, 1, len(folders), 0, 0, 50)

        n = 0
        for i in folders.keys():
            toolboard.board[n][0] = [i, 'DarkRed']
            n += 1

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                        print('ctrl click')
                        self.ctrl_clicked = True

                    if event.key == pg.K_s:
                        if self.ctrl_clicked:
                            print('write')
                            with open('generate map.map', mode='w', encoding='utf-8') as f_out:
                                data = []
                                for line in board.board:
                                    l = []

                                    for val in line:
                                        l.append(','.join(val))

                                    data.append(';'.join(l))

                                f_out.write('\n'.join(data))

                    if self.process == 'entering':
                        if event.key == pg.K_BACKSPACE:
                            if self.process == 'entering' and len(self.params_of_cell[2]) >= 1:
                                self.params_of_cell[2] = self.params_of_cell[2][:-1]

                        elif event.key in range(110000) and chr(event.key) in '1234567890-,':
                            self.params_of_cell[2] += chr(event.key)
                            board.board[self.params_of_cell[0]][self.params_of_cell[1]][2] = self.params_of_cell[2]

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                        self.ctrl_clicked = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos

                        is_action = False
                        if pg.Rect(toolboard.left, toolboard.top, toolboard.width * toolboard.cell_size, toolboard.height * toolboard.cell_size).collidepoint(mouse_pos):
                            is_action = True
                            toolboard.get_click(event.pos, None)
                        elif toolboard.chosen:
                            if pg.Rect(folders[toolboard.chosen].left, folders[toolboard.chosen].top, folders[toolboard.chosen].width * folders[toolboard.chosen].cell_size, folders[toolboard.chosen].height * folders[toolboard.chosen].cell_size).collidepoint(mouse_pos):
                                is_action = True
                                folders[toolboard.chosen].get_click(mouse_pos, None)
                        if not is_action and self.params_of_cell and self.input_rect.collidepoint(mouse_pos):
                            self.process = 'entering'
                            is_action = True
                        if not is_action:
                            board.get_click(mouse_pos, 'get_params')
                            print(self.params_of_cell)
                            if self.params_of_cell is None:
                                is_action = False
                        if not is_action and pg.Rect(board.left, board.top, board.width * board.cell_size, board.height * board.cell_size).collidepoint(mouse_pos):
                            self.process = 'remove board'

                    elif event.button == 4:
                        mouse_pos = event.pos
                        is_action = False
                        if toolboard.chosen:
                            if pg.Rect(folders[toolboard.chosen].left, folders[toolboard.chosen].top, folders[toolboard.chosen].width * folders[toolboard.chosen].cell_size, folders[toolboard.chosen].height * folders[toolboard.chosen].cell_size).collidepoint(mouse_pos):
                                is_action = True
                                if folders[toolboard.chosen].top < 0:
                                    folders[toolboard.chosen].top += self.scrolling
                        if not is_action and pg.Rect(board.left, board.top, board.width * board.cell_size, board.height * board.cell_size).collidepoint(mouse_pos):
                            board.cell_size += self.zoom
                            board.left -= abs(mouse_pos[0] - board.left) / board.cell_size * self.zoom
                            board.top -= abs(mouse_pos[1] - board.top) / board.cell_size * self.zoom

                    elif event.button == 5:
                        mouse_pos = event.pos
                        is_action = False
                        if toolboard.chosen:
                            if pg.Rect(folders[toolboard.chosen].left, folders[toolboard.chosen].top, folders[toolboard.chosen].width * folders[toolboard.chosen].cell_size, folders[toolboard.chosen].height * folders[toolboard.chosen].cell_size).collidepoint(mouse_pos):
                                is_action = True
                                if folders[toolboard.chosen].top + len(folders[toolboard.chosen].board) * folders[toolboard.chosen].cell_size > self.screen_size[1]:
                                    folders[toolboard.chosen].top -= self.scrolling

                        if not is_action and pg.Rect(board.left, board.top, board.width * board.cell_size, board.height * board.cell_size).collidepoint(mouse_pos):
                            board.cell_size -= self.zoom if board.cell_size >= 5 else 0
                            board.left += abs(mouse_pos[0] - board.left) / board.cell_size * self.zoom
                            board.top += abs(mouse_pos[1] - board.top) / board.cell_size * self.zoom

                elif event.type == pg.MOUSEMOTION:
                    if self.process:
                        rel = event.rel
                        if self.process == 'remove board':
                            board.left += rel[0]
                            board.top += rel[1]
                            self.params_of_cell = None
                        elif self.process == 'remove picture':
                            self.x_pict += rel[0]
                            self.y_pict += rel[1]

                elif event.type == pg.MOUSEBUTTONUP:
                    if self.process:
                        if self.process == 'remove board':
                            self.process = ''
                        board.get_click(event.pos, 'get_params')

            if pg.mouse.get_pressed(3)[2]:
                board.get_click(pg.mouse.get_pos(), 'remove pict')
                self.params_of_cell = None

            if pg.key.get_pressed()[pg.K_SPACE]:
                if self.process == 'remove picture':
                    board.get_click(pg.mouse.get_pos(), 'set pict')

            # update

            # render
            self.screen.fill(pg.Color('black'))
            board.render(self.screen)
            toolboard.render(self.screen)
            if toolboard.chosen:
                folders[toolboard.chosen].render(self.screen)
            if self.params_of_cell:
                font = pg.font.Font(pg.font.get_default_font(), 20)
                text_surface = font.render(self.params_of_cell[2], True, pg.Color('white'))
                text_rect = text_surface.get_rect()

                if text_rect.width + 20 < self.input_rect.width:
                    self.input_rect.width = self.width_of_input_rect
                    self.input_rect.x = self.screen_size[0] // 2 - self.width_of_input_rect // 2
                elif text_rect.width + 20 >= self.input_rect.width:
                    self.input_rect.width = text_rect.width + 20
                    self.input_rect.x = self.screen_size[0] // 2 - self.input_rect.width // 2

                pg.draw.rect(self.screen, pg.Color('white'), self.input_rect)
                self.draw_text(self.screen, self.params_of_cell[2], 20, self.screen_size[0] // 2, 75 // 2,
                               pg.Color('black'), pg.font.get_default_font())

                print(self.input_rect.width)
                print(text_rect.width)
            if self.process == 'remove picture':
                self.screen.blit(pg.transform.scale(pg.image.load(self.picture).convert(), (self.wid_pict, self.height_pict)), (self.x_pict, self.y_pict))

            self.clock.tick(self.fps)
            pg.display.flip()
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()
