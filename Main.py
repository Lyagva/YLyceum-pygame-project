from datetime import datetime

import pygame as pg

import Weapon
from states import main_gameplay, menu, levels, quit_, credits, initial_screen


class App:
    def __init__(self):
        # GLOBAL VARS
        self.screen_size = (1080, 720)
        # self.screen_size = (1920, 1080)

        # PG, EVENTS, SCREEN & CLOCK INIT
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.screen_size = pg.display.get_window_size()
        self.screen_rect = pg.Rect(0, 0, self.screen_size[0], self.screen_size[1])  # Это Rect для экрана
        self.events = []

        self.clock = pg.time.Clock()

        self.running = True
        self.FPS = 144
        self.max_fps = 0
        self.show_mouse = True

        # FILES
        self.loot_table = []
        with open('tables/loot_table.table', mode='r', encoding='utf-8') as loot_table:
            self.loot_table = list(map(lambda line: line.split(','), loot_table.read().split('\n')))

        self.weapons_table = []
        with open('tables/weapon.table', mode='r', encoding='utf-8') as loot_table:
            self.weapons_table = list(map(lambda line:
                                          list(map(lambda char:
                                                   list(map(lambda lst_chr: int(lst_chr) if lst_chr.isdigit()
                                                   else lst_chr if list(filter(lambda alp: alp not in '.1234567890',
                                                                               lst_chr)) else float(lst_chr),
                                                            char.split('*')))
                                                   if '*' in char
                                                   else int(char) if char.isdigit() else char
                                                   if list(filter(lambda alp: alp not in '.1234567890',
                                                                  char)) else float(char),
                                                   line.split(','))),
                                          loot_table.read().split('\n')))
        print(self.weapons_table)

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

    def save(self):
        with open(self.states[1].save_file, mode="w+") as file:
            file.seek(0)
            time = str(datetime.now()).split(".")[0]
            print(time, file=file)
            print(self.states[5].player.get_save_data(), file=file)
            print(self.states[5].current_mission, self.states[5].current_sector, file=file)

        print("SUCCESSFULLY SAVED AT:", time)

    def load(self):
        try:
            with open(self.states[1].save_file, mode="r+") as file:
                all_lines = file.readlines()
                self.states[5].save_time = all_lines[0]

                data = all_lines[1]
                data = eval(data)
                # print(type(data), data)
                player = self.states[5].player
                player.health = data[0]
                player.grenades = data[1]

                player.weapons = [Weapon.Weapon(self, self.states[5],
                                                self.states[5].player) for _ in range(len(data[2]))]
                for i in range(len(data[2])):
                    weapon = player.weapons[i]
                    weapon.bullets_per_second = data[2][i][0]
                    weapon.damage = data[2][i][1]
                    weapon.speed = data[2][i][2]
                    weapon.bullets_per_time = data[2][i][3]
                    weapon.distance = data[2][i][4]
                    weapon.spread = data[2][i][5]
                    weapon.ammo = data[2][i][6]
                    weapon.reload_time[1] = data[2][i][7]
                    weapon.bullet_type = data[2][i][8]
                    weapon.image_path = data[2][i][9]
                    weapon.shot_type = data[2][i][10]
                    weapon.source = data[2][i][11]
                    weapon.shoot_cd = [0, 1 / weapon.bullets_per_second]
                    weapon.selected = False
                    weapon.reload_image(weapon.image_path)

                    mods = data[2][i][12]  # Просто массив, как в строке
                    prep_mods = {}  # Готовый к записи массив
                    for k in mods.keys():
                        mod_data = mods[k]
                        print(mod_data)
                        prep_mods[k] = Weapon.WeaponMod(weapon, *mod_data)
                    weapon.mods = prep_mods

                player.money = data[3]
                player.upgrades = data[4]
                player.reload()

                data = list(map(int, all_lines[2].replace("\n", "").split(" ")))
                self.states[5].current_mission, self.states[5].current_sector = data

                print("SUCCESSFULLY LOADED:", self.states[5].save_time)
        except Exception as e:
            print("ERROR WHILE READING SAVE FILE")
            print("ERROR:", e)
            self.stop()


if __name__ == "__main__":
    app = App()
    app.run()
