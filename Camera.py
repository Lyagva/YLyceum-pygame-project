class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, app, main_gameplay):
        self.app = app
        self.main_gameplay = main_gameplay
        self.dx = 0
        self.dy = 0

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

        self.apply(self.main_gameplay.player)

        self.apply(self.main_gameplay.player.weapons[self.main_gameplay.player.selected_weapon])

        for lst in self.main_gameplay.map.map:
            for sprite in lst:
                if sprite is not None:
                    self.apply(sprite)

        for sprite in self.main_gameplay.mobs:
            self.apply(sprite)
            self.apply(sprite.weapons[sprite.selected_weapon])

        for sprite in self.main_gameplay.bullets:
            self.apply(sprite)

        for sprite in self.main_gameplay.explosions:
            self.apply(sprite)

        for sprite in self.main_gameplay.items:
            self.apply(sprite)

