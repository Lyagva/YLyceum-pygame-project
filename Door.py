# Дверь

import pygame as pg

class Door(pg.sprite.Sprite):
    def __init__(self, app, state, map_arg, pos, image=None, trigger_type = "key", trigger_obj_pos = None):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.map = map_arg
        self.x, self.y = pos
        self.type = "door"
        self.trigger_type = trigger_type # key - клавиша f1, button - кнопка (obj), enemies - все враги убиты
        self.trigger_obj_pos = (int(trigger_obj_pos.split(".")[0]) - 1, int(trigger_obj_pos.split(".")[1]) - 1)
        self.trigger_obj = None

        self.rect = pg.Rect(((self.x + 0.25) * self.map.block_size[0],
                             (self.y - 1) * self.map.block_size[1],
                             self.map.block_size[0] * 0.5, self.map.block_size[1] * 2))

        self.image = image
        if self.image:
            self.image = pg.image.load(self.image)
            self.image = pg.transform.scale(self.image, self.rect.size)

        self.opened = True
        self.key_triggered = False

        self.open_time = [0, 0, 1]

    def update(self):
        if self.trigger_type == "lever" and not self.trigger_obj:
            self.trigger_obj = self.map.map[self.trigger_obj_pos[1]][self.trigger_obj_pos[0]]

        self.trigger_op()


        if self.opened == 1:
            self.open_time[0] = min(max(self.open_time[0] + self.app.clock.get_time() / 1000,
                                        self.open_time[1]), self.open_time[2])
        else:
            self.open_time[0] = min(max(self.open_time[0] - self.app.clock.get_time() / 1000,
                                        self.open_time[1]), self.open_time[2])

        self.rect.size = (self.map.block_size[0] * 0.5,
                          self.map.block_size[1] * 2 * 1 / self.open_time[2] * self.open_time[0])

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             (255, 255, 255),
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]


    def trigger_op(self):
        if self.trigger_type == "key":
            if pg.key.get_pressed()[pg.K_F1]:
                if not self.key_triggered:
                    self.opened = -self.opened
                    self.key_triggered = True
            else:
                self.key_triggered = False

        elif self.trigger_type == "lever":
            pressed = self.trigger_obj.get_pressed()
            if pressed:
                self.opened = -1
            else:
                self.opened = 1

        elif self.trigger_type == "enemies":
            if len(self.state.enemies) <= 0:
                self.opened = True
            else:
                self.opened = False


class Lever(pg.sprite.Sprite):
    def __init__(self, app, state, map_arg, pos, image=None):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.map = map_arg
        self.x, self.y = pos
        self.type = "lever"

        self.rect = pg.Rect((self.x * self.map.block_size[0],
                             self.y * self.map.block_size[1],
                             self.map.block_size[0], self.map.block_size[1]))

        self.image = image
        if self.image:
            self.image = pg.image.load(self.image)
            self.image = pg.transform.scale(self.image, self.rect.size)

        self.enabled = -1
        self.pressed = False

        pg.font.init()
        self.text = pg.font.SysFont("serif", 24).render('"E"', True, (255, 255, 255))

    def update(self):
        if pg.sprite.collide_rect(self, self.state.player):
            if pg.key.get_pressed()[pg.K_e]:
                if not self.pressed:
                    self.pressed = True
                    self.enabled = -self.enabled
            else:
                self.pressed = False


    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                if self.enabled == 1:
                    pg.draw.rect(self.app.screen,
                                 (0, 255, 0),
                                 self.rect)
                else:
                    pg.draw.rect(self.app.screen,
                                 (255, 0, 0),
                                 self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

            if self.rect.colliderect(self.state.player.rect):
                self.app.screen.blit(self.text, (self.state.player.rect.center[0] - self.text.get_width() / 2,
                                                 self.state.player.rect.top - self.text.get_height()))

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]

    def get_pressed(self):
        return True if self.enabled == 1 else False