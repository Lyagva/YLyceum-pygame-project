# Камера

import pygame as pg

def clamp(x, mi, ma):
    return min(max(x, mi), ma)


class Camera:
    def __init__(self, app, state):
        self.app = app
        self.state = state

        self.follow_player = True
        self.follow_mouse = True
        self.speed_mult = 0.5
        self.delta_pos = (0, 0)
        self.mouse_div = 4

    def update(self):
        self.delta_pos = (0, 0)
        player = self.state.player.rect.center
        mouse = pg.mouse.get_pos()

        if self.follow_player:
            delta_player = (player[0] - self.app.screen_size[0] / 2,
                            player[1] - self.app.screen_size[1] / 2)
            self.delta_pos = (int(delta_player[0] * self.speed_mult),
                                  int(delta_player[1] * self.speed_mult))
            self.move(self.delta_pos)

        if self.follow_mouse:
            delta_mouse = ((player[0] + mouse[0] - self.app.screen_size[0]) / self.mouse_div,
                           (player[1] + mouse[1] - self.app.screen_size[1]) / self.mouse_div)

            self.delta_pos = (int(delta_mouse[0]),
                              int(delta_mouse[1]))

            self.move(self.delta_pos)

    def move(self, delta_pos):
        self.state.map.map_move(delta_pos)

        for item in self.state.items:
            item.move(delta_pos)

        self.state.player.move(delta_pos)
        for item in self.state.player.weapons:
            item.move(self.delta_pos)

        for item in self.state.bullets:
            item.move(delta_pos)
        for item in self.state.grenades:
            item.move(delta_pos)
        for item in self.state.explosions:
            item.move(delta_pos)