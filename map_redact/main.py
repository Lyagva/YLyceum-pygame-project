import pygame as pg
import imghdr
import os


class Board:
    # создание поля
    def __init__(self, app, width, height, left, top, cell_size):
        self.app = app

        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for col in range(self.height):
            for row in range(self.width):
                if self.board[col][row] == 0:
                    pg.draw.rect(screen, pg.Color("white"),
                                 (row * self.cell_size + self.left, col * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)
                else:
                    screen.blit(pg.transform.scale(pg.image.load(self.board[col][row]).convert(),
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
        if cell:
            self.on_click(cell, func)

    def on_click(self, cell, func):
        print(cell)
        if func == 'set pict':
            self.board[int(cell[0])][int(cell[1])] = self.app.picture
        elif func == 'remove pict':
            self.board[int(cell[0])][int(cell[1])] = 0


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
                except IndexError:
                    pass

    def on_click(self, cell, unuse):
        self.app.process = 'remove picture'
        self.app.picture = self.board[cell[0]][cell[1]]
        self.app.x_pict, self.app.y_pict, self.app.wid_pict, self.app.height_pict = cell[1] * self.cell_size + self.left, \
                                                                                    cell[0] * self.cell_size + self.top, \
                                                                                    self.cell_size, self.cell_size


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
        self.click_timer = 0

        self.picture = None
        self.x_pict, self.y_pict, self.wid_pict, self.height_pict = None, None, None, None

        self.fps = 120
        self.running = True

    def run(self):
        board = Board(self, 50, 50, 100, 100, 20)

        folders = dict()
        for dirpath, dirnames, filenames in os.walk('platformer art/Base pack'):
            print(dirpath, dirnames, sep='    ')
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

                        if not is_action and pg.Rect(board.left, board.top, board.width * board.cell_size, board.height * board.cell_size).collidepoint(mouse_pos):
                            self.process = 'remove board'

                    elif event.button == 3:
                        if self.click_timer == 0:
                            self.click_timer = 0.001
                        elif self.click_timer < 0.5:
                            board.get_click(event.pos, 'remove pict')
                            self.click_timer = 0

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
                        elif self.process == 'remove picture':
                            self.x_pict += rel[0]
                            self.y_pict += rel[1]

                elif event.type == pg.MOUSEBUTTONUP:
                    if self.process:
                        if self.process == 'remove board':
                            self.process = ''
                        elif self.process == 'remove picture':
                            board.get_click(event.pos, 'set pict')
                            self.process = ''
                            self.picture = None
                            self.x_pict, self.y_pict, self.wid_pict, self.height_pict = None, None, None, None

            # render
            if self.click_timer != 0:
                self.click_timer += 0.5 / self.fps
                if self.click_timer >= 0.5:
                    timer = 0

            self.screen.fill(pg.Color('black'))
            board.render(self.screen)
            toolboard.render(self.screen)

            if toolboard.chosen:
                folders[toolboard.chosen].render(self.screen)
            if self.process == 'remove picture':
                self.screen.blit(pg.transform.scale(pg.image.load(self.picture).convert(), (self.wid_pict, self.height_pict)), (self.x_pict, self.y_pict))

            self.clock.tick(self.fps)
            pg.display.flip()
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()
