# Кнопка, рычаг или типо того

import pygame as pg

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