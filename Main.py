# Это главный класс, тут есть app. Это класс окна. Дофига важно.

# Импорт библиотек
import pygame as pg

# Импорт классов
import Map
import Player
import Block
import Weapon


class App:
    def __init__(self):
        # GLOBAL VARS
        self.screen_size = (1080, 720)
        self.running = True
        self.FPS = 1000

        # PG, SCREEN & CLOCK INIT
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.screen_rect = pg.Rect(0, 0, self.screen_size[0], self.screen_size[1]) # Это Rect для экрана

        self.clock = pg.time.Clock()

        # PLAYER
        self.player = Player.Player(self)

        # MAP
        self.map = Map.Map(self)


    def run(self):
        while self.running:
            # EVENTS ================================
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # UPDATE ================================
            self.map.update()
            self.player.update()

            # RENDER ================================
            self.screen.fill((0, 0, 0))

            # Map
            self.map.render()

            # Player
            self.player.render()

            pg.display.flip()


            # OTHER PROCESSES ================================
            self.clock.tick(self.FPS)
            pg.display.set_caption("FPS: " + str(self.clock.get_fps() * 100 // 1 / 100))

        pg.quit()


if __name__ == "__main__":
    app = App()
    app.run()