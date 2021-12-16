import pygame as pg
import imghdr
import os


class Board:
    # создание поля
    def __init__(self, width, height, left, top, cell_size):
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
        print(cell)


class Images:
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

        self.board = [self.images[i] for i in range(self.height)]

    def render(self, screen):
        for col in range(self.height):
            if self.board[col]:
                x, y = self.left, col * self.cell_size + self.top
                if self.app.screen_rect.collidepoint((x, y)):
                    screen.blit(pg.transform.scale(pg.image.load(self.board[col]).convert(), (self.cell_size, self.cell_size)),
                                (x, y))


class Buttons(Board):
    def __init__(self, width, height, left, top, cell_size):
        super().__init__(width, height, left, top, cell_size)
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

    def on_click(self, cell):
        print(cell)
        for col in range(self.height):
            for row in range(self.width):
                if (col, row) == cell:
                    self.board[col][row][1] = 'red'
                    self.chosen = self.board[col][row][0]
                else:
                    self.board[col][row][1] = 'DarkRed'


class App:
    def __init__(self):
        pg.init()
        self.screen_size = (1000, 500)
        self.screen = pg.display.set_mode(self.screen_size)
        self.clock = pg.time.Clock()

        self.screen_rect = pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])

        self.zoom = 0.5
        self.scrolling = 100
        self.process = None
        self.fps = 120
        self.running = True

    def run(self):
        board = Board(50, 50, 100, 100, 20)

        toolboard = Buttons(1, 3, 0, 0, 50)
        toolboard.board[0][0] = ['Blocks', 'DarkRed']
        toolboard.board[1][0] = ['Mobs', 'DarkRed']
        toolboard.board[2][0] = ['Players', 'DarkRed']

        blocks = Images(self, 50, 0, 50, 'platformer Art/Base pack/Tiles')

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        if pg.Rect(toolboard.left, toolboard.top, toolboard.width * toolboard.cell_size, toolboard.height * toolboard.cell_size).collidepoint(mouse_pos):
                            toolboard.get_click(event.pos)
                        elif pg.Rect(board.left, board.top, board.width * board.cell_size, board.height * board.cell_size).collidepoint(mouse_pos):
                            self.process = 'remove board'

                    elif event.button == 4:
                        mouse_pos = event.pos
                        if toolboard.chosen == 'Blocks':
                            if pg.Rect(blocks.left, blocks.top, blocks.width * blocks.cell_size,
                                       blocks.height * blocks.cell_size).collidepoint(mouse_pos):
                                blocks.top -= self.scrolling if len(blocks.board) * blocks.cell_size + blocks.top > self.screen_size[1] else 0
                        elif pg.Rect(board.left, board.top, board.width * board.cell_size,
                                     board.height * board.cell_size).collidepoint(mouse_pos):
                            board.cell_size += self.zoom

                    elif event.button == 5:
                        mouse_pos = event.pos
                        if toolboard.chosen == 'Blocks':
                            if pg.Rect(blocks.left, blocks.top, blocks.width * blocks.cell_size,
                                       blocks.height * blocks.cell_size).collidepoint(mouse_pos):
                                blocks.top += self.scrolling if blocks.top < 0 else 0
                        if pg.Rect(board.left, board.top, board.width * board.cell_size,
                                   board.height * board.cell_size).collidepoint(mouse_pos):
                            board.cell_size -= self.zoom

                elif event.type == pg.MOUSEMOTION:
                    if self.process:
                        rel = event.rel
                        if self.process == 'remove board':
                            board.left += rel[0]
                            board.top += rel[1]

                elif event.type == pg.MOUSEBUTTONUP:
                    if self.process:
                        if self.process == 'remove board':
                            self.process = ''

            # render

            self.screen.fill(pg.Color('black'))
            board.render(self.screen)
            toolboard.render(self.screen)

            if toolboard.chosen == 'Blocks':
                blocks.render(self.screen)

            self.clock.tick(self.fps)
            pg.display.flip()
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.run()