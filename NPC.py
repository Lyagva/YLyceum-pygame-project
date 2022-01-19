from PickUp import ItemEmpty
import pygame as pg


class NPC(ItemEmpty):
    def __init__(self, app, state, map, pos, actions, image=None, type="anvil"):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.map = map
        self.x, self.y = pos
        self.actions = actions
        self.type = type

        self.image1 = None
        self.image2 = None
        if self.type == "anvil":
            self.rect = pg.Rect((self.x * self.map.block_size[0],
                                 (self.y - 3) * self.map.block_size[1],
                                 self.map.block_size[0] * 4, self.map.block_size[1] * 4))

            self.image1 = pg.image.load("images/entities/Anvil1.png")
            self.image1 = pg.transform.scale(self.image1, self.rect.size)

            self.image2 = pg.image.load("images/entities/Anvil2.png")
            self.image2 = pg.transform.scale(self.image2, self.rect.size)
        else:
            self.rect = pg.Rect((self.x * self.map.block_size[0],
                                 (self.y - 2) * self.map.block_size[1],
                                 self.map.block_size[0] * 3, self.map.block_size[1] * 3))

            self.image1 = pg.image.load("images/entities/BioTrader.png")
            self.image1 = pg.transform.scale(self.image1, self.rect.size)

            self.image2 = self.image1.copy()

        self.timer = [0, 1]

        self.color = (192, 255, 192)
        self.need_e = True

        self.text = self.app.font.render('"E"', True, (255, 255, 255))

    def update(self):
        self.timer[0] += self.app.clock.get_time() / 1000 * self.timer[1]
        if self.timer[0] >= 2:
            self.timer[0] = 0

        if self.rect.colliderect(self.state.player.rect) and \
                (pg.key.get_pressed()[pg.K_e] or not self.need_e):
            self.on_pickup()

    def render(self):
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image1:
                pg.draw.rect(self.app.screen,
                             self.color,
                             self.rect)
            else:
                if self.timer[0] <= 1:
                    self.app.screen.blit(self.image1, self.rect)
                else:
                    self.app.screen.blit(self.image2, self.rect)

            if self.rect.colliderect(self.state.player.rect):
                self.app.screen.blit(self.text, (self.state.player.rect.center[0] - self.text.get_width() / 2,
                                                 self.state.player.rect.top - self.text.get_height()))

    def on_pickup(self):
        exec(self.actions)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]