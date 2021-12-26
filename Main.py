import pygame as pg

from states import main_gameplay, menu, levels, quit_, credits


class App:
    def __init__(self):
        # GLOBAL VARS
        self.screen_size = (1080, 720)
        # self.screen_size = (1920, 1080)

        self.running = True
        self.FPS = 144
        self.max_fps = 0
        self.show_mouse = True

        # STATE SYSTEM
        self.state = 1
        self.states = [quit_.Quit(self),
                       menu.Menu(self),
                       levels.Levels(self),
                       None,  # Настройки
                       credits.Credits(self),  # Авторы
                       main_gameplay.MainGameplay(self)]

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
                    if self.state == 1:
                        self.stop()
                    elif self.state in [2, 3, 4, 5]:
                        self.state = 1

            # UPDATE ================================
            self.show_mouse = True
            self.states[self.state].update()

            # RENDER ================================
            pg.mouse.set_visible(self.show_mouse)
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
