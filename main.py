import pygame as pg


from states import main_gameplay, menu, levels


class App:
    def __init__(self):
        # GLOBAL VARS
        self.screen_size = (1080, 720)
        self.running = True
        self.FPS = 144
        self.max_fps = 0

        # STATE SYSTEM
        self.state = 1
        self.states = [main_gameplay.MainGameplay(self), menu.Menu(self), levels.Levels(self)]

        # PG, EVENTS, SCREEN & CLOCK INIT
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.screen_rect = pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])  # Это Rect для экрана
        self.events = []

        self.clock = pg.time.Clock()

    def run(self):
        while self.running:
            # EVENTS ================================
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    self.running = False
                    print("MAX FPS:", self.max_fps)

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
