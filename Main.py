import pygame as pg

from states import main_gameplay, menu, levels, quit_, credits, initial_screen


class App:
    def __init__(self):
        # GLOBAL VARS
        self.screen_size = (1080, 720)
        #self.screen_size = (1920, 1080)

        self.running = True
        self.FPS = 144
        self.max_fps = 0

        # FILES
        self.loot_table = []
        with open('loot_table.table', mode='r', encoding='utf-8') as loot_table:
            self.loot_table = list(map(lambda line: line.split(','), loot_table.read().split('\n')))

        # STATE SYSTEM
        self.state = 6
        self.states = [quit_.Quit(self),
                       menu.Menu(self),
                       levels.Levels(self),
                       None,  # Настройки
                       credits.Credits(self),  # Авторы
                       main_gameplay.MainGameplay(self),
                       initial_screen.InitialScreen(self)  # заставка
                       ]

        # PG, EVENTS, SCREEN & CLOCK INIT
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.screen_rect = pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])  # Это Rect для экрана
        self.events = []

        self.clock = pg.time.Clock()

    def stop(self):
        self.running = False
        print("MAX FPS:", self.max_fps)

    def run(self):
        while self.running:
            # EVENTS ================================
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    self.stop()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.stop()

            # UPDATE ================================
            self.states[self.state].update()

            # RENDER ================================
            self.screen.fill((0, 0, 0))

            self.states[self.state].render()

            pg.display.flip()

            # OTHER PROCESSES ================================
            self.clock.tick(self.FPS)
            pg.display.set_caption("FPS: " + str(self.clock.get_fps() * 100 // 1 / 100))
            self.max_fps = max(self.max_fps, self.clock.get_fps())

        pg.quit()


if __name__ == "__main__":
    app = App()
    app.run()
