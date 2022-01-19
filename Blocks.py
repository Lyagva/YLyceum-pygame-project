# Это класс с базовой структурой блока. У него есть коллизия и текстура.

# Импорт библиотек
import pygame as pg


class Block(pg.sprite.Sprite):
    # Позиция идёт относительная, то есть это не координаты на экране, а координаты карты
    def __init__(self, app, map_arg, pos, image=None, type="block", size=(1, 1)):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.map = map_arg
        self.x, self.y = pos
        self.type = type

        self.rect = pg.Rect((self.x * self.map.block_size[0] - self.map.map_offset[0],
                             self.y * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0] * size[0], self.map.block_size[1] * size[1]))

        self.image = image
        if self.image:
            self.image = pg.image.load(self.image)
            self.image = pg.transform.scale(self.image, self.rect.size)

    def update(self):
        pass

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             (0, 32 + ((255 - 32) / self.map.map_size[0] * self.x),
                              32 + ((255 - 32) / self.map.map_size[1] * self.y)),  # Тут просто градиентик
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]


class DestroyableBlock(pg.sprite.Sprite):
    # Позиция идёт относительная, то есть это не координаты на экране, а координаты карты
    def __init__(self, app, map_arg, pos, image=None, health=100):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.map = map_arg
        self.x, self.y = pos
        self.type = "destroyableblock"

        self.rect = pg.Rect((self.x * self.map.block_size[0] - self.map.map_offset[0],
                             self.y * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))

        self.image = pg.image.load("images/block/subtitle4.png")
        self.image = pg.transform.scale(self.image, self.rect.size)

        self.health = health

    def update(self):
        if self.health != "inf" and self.health <= 0:
            for row in range(self.map.map_size[1]):
                for col in range(self.map.map_size[0]):
                    if self.map.map[row][col] == self:
                        self.map.map[row][col] = None

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if not self.image:
                pg.draw.rect(self.app.screen,
                             (128, 85, 64),
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]

    def get_damage(self, damage):
        if self.health != "inf":
            self.health -= damage


class ForceField(pg.sprite.Sprite):
    def __init__(self, app, map_arg, pos, image=None, health=100):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.map = map_arg
        self.x, self.y = pos
        self.type = "forcefield"

        self.rect = pg.Rect((self.x * self.map.block_size[0] - self.map.map_offset[0],
                             self.y * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))

        self.image1 = pg.image.load("images/entities/ForceField1.png")
        self.image1 = pg.transform.scale(self.image1, self.rect.size)

        self.image2 = pg.image.load("images/entities/ForceField2.png")
        self.image2 = pg.transform.scale(self.image2, self.rect.size)

        self.health = health
        self.timer = [0, 4]

    def update(self):
        self.timer[0] += self.app.clock.get_time() / 1000 * self.timer[1]
        if self.timer[0] >= 2:
            self.timer[0] = 0

        if self.health != "inf" and self.health <= 0:
            for row in range(self.map.map_size[1]):
                for col in range(self.map.map_size[0]):
                    if self.map.map[row][col] == self:
                        self.map.map[row][col] = None

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if self.timer[0] <= 1:
                self.app.screen.blit(self.image1, self.rect)
            else:
                self.app.screen.blit(self.image2, self.rect)

    def get_damage(self, damage):
        if self.health != "inf":
            self.health -= damage

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]


class JumpPad(pg.sprite.Sprite):
    def __init__(self, app, map_arg, pos, image=None, force=10):
        pg.sprite.Sprite.__init__(self)
        self.app = app
        self.map = map_arg
        self.x, self.y = pos
        self.type = "jumppad"

        self.rect = pg.Rect((self.x * self.map.block_size[0] - self.map.map_offset[0],
                             self.y * self.map.block_size[1] - self.map.map_offset[1],
                             self.map.block_size[0], self.map.block_size[1]))

        self.image = pg.image.load("images/entities/Jumppad.png")
        self.image = pg.transform.scale(self.image, self.rect.size)

        self.force = force

    def update(self):
        pass

    def render(self):
        # Проверка нужно ли отрисовывать блок (Или он за экраном и это не надо делать)
        if self.app.screen_rect.colliderect(self.rect):
            if self.image is None:
                pg.draw.rect(self.app.screen,
                             (0, 255, 0),
                             self.rect)
            else:
                self.app.screen.blit(self.image, self.rect)

    def move(self, delta_pos):
        self.rect.x -= delta_pos[0]
        self.rect.y -= delta_pos[1]


class Ladder(Block):
    def __init__(self, app, map_arg, pos, image=None):
        super().__init__(app, map_arg, pos, image)
        self.type = "stairs"

        self.image1 = pg.image.load("images/entities/Ladder1.png")
        self.image1 = pg.transform.scale(self.image1, self.rect.size)

        self.image2 = pg.image.load("images/entities/Ladder2.png")
        self.image2 = pg.transform.scale(self.image2, self.rect.size)

        self.timer = [0, 4]

    def update(self):
        self.timer[0] += self.app.clock.get_time() / 1000 * self.timer[1]
        if self.timer[0] >= 2:
            self.timer[0] = 0

    def render(self):
        if self.app.screen_rect.colliderect(self.rect):
            if self.timer[0] <= 1:
                self.app.screen.blit(self.image1, self.rect)
            else:
                self.app.screen.blit(self.image2, self.rect)


class Lava(Block):
    def __init__(self, app, map_arg, pos, image=None, damage=1, collide=True):
        super().__init__(app, map_arg, pos, image)

        self.type = "lava"
        self.is_collide = collide
        self.damage = damage

        self.image1 = pg.image.load("images/entities/Lava1.png")
        self.image1 = pg.transform.scale(self.image1, self.rect.size)

        self.image2 = pg.image.load("images/entities/Lava2.png")
        self.image2 = pg.transform.scale(self.image2, self.rect.size)

        self.image3 = pg.image.load("images/entities/Lava3.png")
        self.image3 = pg.transform.scale(self.image3, self.rect.size)

        self.image4 = pg.image.load("images/entities/Lava4.png")
        self.image4 = pg.transform.scale(self.image4, self.rect.size)

        self.timer = [0, 4]

    def update(self):
        self.timer[0] += self.app.clock.get_time() / 1000 * self.timer[1]
        if self.timer[0] >= 4:
            self.timer[0] = 0

    def render(self):
        if self.app.screen_rect.colliderect(self.rect):
            if self.timer[0] <= 1:
                self.app.screen.blit(self.image1, self.rect)
            elif self.timer[0] <= 2:
                self.app.screen.blit(self.image2, self.rect)
            elif self.timer[0] <= 3:
                self.app.screen.blit(self.image3, self.rect)
            else:
                self.app.screen.blit(self.image4, self.rect)
