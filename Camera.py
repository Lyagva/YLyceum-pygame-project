from Functions import *

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, app, state):
        self.app = app
        self.state = state
        self.dx = 0
        self.dy = 0
        self.mouse_k = 2

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.app.screen_size[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.app.screen_size[1] // 2)

    def mega_apply(self, apply_rect):
        self.apply(apply_rect)

        self.apply(self.state.player)

        self.apply(self.state.player.weapons[self.state.player.selected_weapon])

        for lst in self.state.map.map:
            for sprite in lst:
                if sprite is not None:
                    self.apply(sprite)

        for sprite in self.state.mobs:
            self.apply(sprite)

            self.apply(sprite.weapons[sprite.selected_weapon])
            if not sprite.player_is_visible:
                sprite.weapons[sprite.selected_weapon].bullet_vector = ((sprite.rect.centerx + 10 if sprite.turn_to == 'right' else sprite.rect.centerx - 10), sprite.rect.centery)
            else:
                sprite.weapons[sprite.selected_weapon].bullet_vector = self.state.player.rect.center

        for sprite in self.state.bullets:
            sprite.pos = (sprite.pos[0] + self.dx, sprite.pos[1] + self.dy)
            self.apply(sprite)

        for sprite in self.state.explosions:
            sprite.pos = (sprite.pos[0] + self.dx, sprite.pos[1] + self.dy)
            self.apply(sprite)

        for sprite in self.state.grenades:
            self.apply(sprite)

        for sprite in self.state.items:
            self.apply(sprite)

        for sprite in self.state.stairs:
            self.apply(sprite)

        for sprite in self.state.npcs:
            self.apply(sprite)

