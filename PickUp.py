# Подбираемый айтем

import pygame as pg


class ItemEmpty(pg.sprite.Sprite):
    def __init__(self, app, state, map, pos, image=None):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.state = state
        self.map = map
        self.x, self.y = pos

        self.rect = pg.Rect(((self.x + 0.3) * self.map.block_size[0],
                             (self.y + 0.3) * self.map.block_size[1],
                             self.map.block_size[0] * 0.4, self.map.block_size[1] * 0.4))

        self.image = image
        if self.image:
            self.image = pg.image.load(self.image)
            self.image = pg.transform.scale(self.image, self.rect.size)

        self.color = (255, 255, 255)
        self.need_e = True

        self.text = pg.font.SysFont("serif", 24).render('"E"', True, (255, 255, 255))

    def update(self):
        if self.rect.colliderect(self.state.player.rect) and \
                (pg.key.get_pressed()[pg.K_e] or not self.need_e):
            self.on_pickup()

    def render(self):
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             self.color,
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

            if self.rect.colliderect(self.state.player.rect):
                self.app.screen.blit(self.text, (self.state.player.rect.center[0] - self.text.get_width() / 2,
                                                 self.state.player.rect.top - self.text.get_height()))

    def on_pickup(self):
        self.kill()

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]


class ItemMedKit(ItemEmpty):
    def __init__(self, app, state, map, pos, dhp=None, image=None):
        super(ItemMedKit, self).__init__(app, state, map, pos, image)
        self.color = (0, 255, 0)

        if dhp:
            self.dhp = dhp
        else:
            self.dhp = 10

    def update(self):
        if self.rect.colliderect(self.state.player.rect) and \
                ((pg.key.get_pressed()[pg.K_e] or not self.need_e) or
                self.state.player.health[1] - self.state.player.health[0] >= self.dhp):
            self.on_pickup()

    def on_pickup(self):
        if self.state.player.health[0] < self.state.player.health[1]:
            self.state.player.health[0] += self.dhp
            self.kill()


class ItemAmmo(ItemEmpty):
    def __init__(self, app, state, map, pos, ammo=None, image=None): # ammo в процентах
        super(ItemAmmo, self).__init__(app, state, map, pos, image)
        self.color = (241, 196, 15)
        if ammo:
            self.ammo = ammo
        else:
            self.ammo = 10


    def on_pickup(self):
        weapon = self.state.player.weapons[self.state.player.selected_weapon]
        if weapon.ammo[2] < weapon.ammo[3]:
            self.state.player.weapons[self.state.player.selected_weapon].ammo[2] += \
                int(self.state.player.weapons[self.state.player.selected_weapon].ammo[3] * self.ammo / 100)

            self.kill()


class ItemGrenade(ItemEmpty):
    def __init__(self, app, state, map, pos, image=None):
        super(ItemGrenade, self).__init__(app, state, map, pos, image)
        self.need_e = False
        self.color = (39, 174, 96)

    def on_pickup(self):
        if self.state.player.grenades[0] < self.state.player.grenades[1]:
            self.state.player.grenades[0] += 1

            self.kill()


class ItemWeapon(ItemEmpty):
    def __init__(self, app, state, map, pos, weapon):
        super(ItemWeapon, self).__init__(app, state, map, pos, None)
        self.rect = pg.Rect(self.x - self.map.block_size[0] / 4, self.y - self.map.block_size[1] / 4,
                            self.map.block_size[0] / 2, self.map.block_size[1] / 2)
        print(self.x, self.y)
        self.weapon = weapon
        self.color = (0, 255, 255)

    def render(self):
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             self.color,
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

            if self.rect.colliderect(self.state.player.rect):
                self.app.screen.blit(self.text, (self.state.player.rect.center[0] - self.text.get_width() / 2,
                                                 self.state.player.rect.top - self.text.get_height()))

    def on_pickup(self):
        if len(self.state.player.weapons) < 3:
            self.state.player.selected_weapon = len(self.state.player.weapons)
            self.state.player.weapons.append(self.weapon)
        else:
            self.state.items.add(ItemWeapon(self.app, self.state, self.map, (self.rect.x, self.rect.y),
                                            self.state.player.weapons[self.state.player.selected_weapon]))
            self.state.player.weapons[self.state.player.selected_weapon] = self.weapon

        self.kill()


class ItemWeaponMod(ItemEmpty):
    def __init__(self, app, state, map, pos, mod, image=None):
        super(ItemWeaponMod, self).__init__(app, state, map, pos, image)
        self.rect = pg.Rect(self.rect.x - self.map.block_size[0] / 4, self.rect.y - self.map.block_size[1] / 4,
                            self.map.block_size[0] / 2, self.map.block_size[1] / 2)
        print(self.x, self.y)
        self.mod = mod
        self.color = (0, 0, 255)

    def render(self):
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             self.color,
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

            if self.rect.colliderect(self.state.player.rect):
                self.app.screen.blit(self.text, (self.state.player.rect.center[0] - self.text.get_width() / 2,
                                                 self.state.player.rect.top - self.text.get_height()))

    def on_pickup(self):
        slot = self.mod.slot
        weapon = self.state.player.weapons[self.state.player.selected_weapon]

        if weapon.mods[slot].lvl == [0, 0]:
            self.mod.weapon = weapon
            weapon.mods[slot] = self.mod

            self.kill()
