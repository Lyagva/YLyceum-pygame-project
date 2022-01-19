import pygame as pg

from PickUp import ItemEmpty


class Teleport(ItemEmpty):
    def __init__(self, app, state, map, pos, type="level", image=None):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.map = map
        self.x, self.y = pos
        self.type = type

        self.rect = pg.Rect((self.x * self.map.block_size[0],
                             (self.y - 3) * self.map.block_size[1],
                             self.map.block_size[0] * 2, self.map.block_size[1] * 4))

        self.image = pg.image.load("images/entities/Teleport.png")
        self.image = pg.transform.scale(self.image, self.rect.size)

        self.color = (128, 255, 255)
        self.need_e = True

        self.text = self.app.font.render('"E"', True, (255, 255, 255))

    def update(self):
        if self.rect.colliderect(self.state.player.rect) and \
                (pg.key.get_pressed()[pg.K_e] or not self.need_e):
            self.on_pickup()

    def render(self):
        self.app.screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.colliderect(self.state.player.rect):
            self.app.screen.blit(self.text, (self.state.player.rect.centerx - self.text.get_size()[0] / 2,
                                             self.state.player.rect.y - self.text.get_size()[1]))

    def on_pickup(self):
        if self.type == "level":
            self.state.switch_window(3)
        else:
            self.state.switch_window(2)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]
