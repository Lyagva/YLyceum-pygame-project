# Класс карты. Ну тут храниться матрица блоков
"""
Формат карты предлагаю использовать такой:
    Первая строка - Информация:
        ширина, высота

    Матрица, где одна строчка - одна строчка массива, а все элементы разделены ";".
    Все пробелы просто будем очищать.

    Каждый элемент:
        <Тип (блок, сущность и т.д.)>,<Чё нибудь ещё>;

        Пример блока:
            block,1.png;

        В аргументах, разделитель(для списков) - "|", а запятая меняется на "^";

Пример матрицы:

4 5
block,1.png;block,1.png;block,1.png;block,1.png
block,1.png;           ;           ;block,1.png
block,1.png;           ;           ;block,1.png
block,1.png;           ;           ;block,1.png
block,1.png;block,1.png;block,1.png;block,1.png
"""

# Импорт библиотек
# ???

# Импорт классов
import Blocks
import Door
import NPC
import PickUp
import PlayerSpawn
import Mob
import Danger_block
import Teleport
import Weapon


class Map:
    def __init__(self, app, state, file="maps/3.map"):
        self.app = app
        self.file = file
        self.state = state

        self.map_offset = (0, 0)  # Смещение всей карты в пикселях (К примеру при движении персонажа)
        # К примеру: при (100, 0) начала карты уедет на 100 пикс. ВЛЕВО, как при ходьбе в ПРАВО

        self.map_size = (100, 20)  # Размер карты в блок
        self.blocks_per_screen = 14
        self.block_size = (self.app.screen_size[1] / self.blocks_per_screen // 1,
                           self.app.screen_size[1] / self.blocks_per_screen // 1)  # Размер блока в пикселях

        # (Вначале y, а потом x)
        self.map = [[None
                     for _ in range(self.map_size[0])]
                    for _ in range(self.map_size[1])]

        self.read_file()

    def update(self):
        # Вначале y, а потом x
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                if self.map[row][col]:
                    if self.map[row][col] != "playerspawn":
                        self.map[row][col].update()

    def render(self):
        # Вначале y, а потом x
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                if self.map[row][col]:
                    if self.map[row][col] != "playerspawn":
                        self.map[row][col].render()

    def read_file(self):
        self.map = []
        self.state.items.empty()
        self.state.npcs.empty()
        self.state.mobs.empty()
        self.state.stairs.empty()

        with open(self.file) as file:
            raw_data = file.readlines()
        self.map_size = (int(raw_data[0].split()[0]), int(raw_data[0].split()[1]))  # ширина, выоста
        no_spaces_data = ["".join([i for i in line if i != " "]).replace("\n", "")
                          for line in raw_data[1:]]  # Очистка от пробелов

        clear_data = [[i for i in line.split(";")]
                      for line in no_spaces_data]  # Подводка

        # Тут мы добаляем все элементы
        for y in range(self.map_size[1]):
            self.map.append([])
            for x in range(self.map_size[0]):
                if y < len(clear_data) and x < len(clear_data[y]):
                    # Получение аргументов
                    args = clear_data[y][x].split(",")[1:]

                    if len(args) > 0:
                        img = args[0]
                    else:
                        img = None

                    if clear_data[y][x].split(",")[0] == "block":  # Статичный блок
                        if len(args) > 1:
                            type = args[1]
                        else:
                            type = "block"

                        if len(args) > 3 and args[2] != "":
                            size = tuple(map(int, args[2:]))
                        else:
                            size = (1, 1)

                        self.map[y].append(Blocks.Block(self.app, self, (x, y), img, type, size))

                    elif clear_data[y][x].split(",")[0] == "jumppad":  # Батут
                        if len(args) > 1:
                            force = args[1]
                        else:
                            force = 10

                        self.map[y].append(Blocks.JumpPad(self.app, self, (x, y), img, int(force)))

                    elif clear_data[y][x].split(",")[0] == "forcefield":  # Силовое поле
                        if len(args) > 1:
                            health = args[1]
                        else:
                            health = 100

                        self.map[y].append(Blocks.ForceField(self.app, self, (x, y), img, health))

                    elif clear_data[y][x].split(",")[0] == "destroyableblock":  # Разрушаемый блок
                        if len(args) > 1 and args[1] != "":
                            health = args[1]
                        else:
                            health = 100

                        self.map[y].append(Blocks.DestroyableBlock(self.app, self, (x, y), img, health))

                    elif clear_data[y][x].split(",")[0] == "playerspawn":
                        self.map[y].append(PlayerSpawn.PlayerSpawn(self.app, self.state,
                                                                   (self.block_size[0] * x, self.block_size[1] * y)))

                    elif clear_data[y][x].split(",")[0] == "door":  # Статичный блок
                        if len(args) > 1:
                            trigger_type = args[1]
                        else:
                            trigger_type = "key"

                        if len(args) > 2 and args[2] != "":
                            trigger_obj_pos = args[2]
                        else:
                            trigger_obj_pos = None

                        self.map[y].append(Door.Door(self.app, self.state, self, (x, y), img,
                                                     trigger_type=trigger_type, trigger_obj_pos=trigger_obj_pos))

                    elif clear_data[y][x].split(",")[0] == "lever":
                        self.map[y].append(Door.Lever(self.app, self.state, self, (x, y), img))

                    elif clear_data[y][x].split(",")[0].split("_")[0] == "pickup":
                        self.map[y].append(None)

                        if clear_data[y][x].split(",")[0].split("_")[1] == "empty":
                            self.state.items.add(PickUp.ItemEmpty(self.app, self.state, self,
                                                                  (x, y), image=img))
                        if clear_data[y][x].split(",")[0].split("_")[1] == "medkit":
                            if len(args) > 1:
                                dhp = int(args[1])
                            else:
                                dhp = None

                            self.state.items.add(PickUp.ItemMedKit(self.app, self.state, self,
                                                                   (x, y), image=img, dhp=dhp))
                        if clear_data[y][x].split(",")[0].split("_")[1] == "ammo":
                            if len(args) > 1:
                                ammo = int(args[1])
                            else:
                                ammo = None

                            self.state.items.add(PickUp.ItemAmmo(self.app, self.state, self,
                                                                 (x, y), image=img, ammo=ammo))

                        if clear_data[y][x].split(",")[0].split("_")[1] == "grenade":
                            self.state.items.add(PickUp.ItemGrenade(self.app, self.state, self,
                                                                    (x, y), image=img))

                        if clear_data[y][x].split(",")[0].split("_")[1] == "weaponmod":
                            if len(args) > 1:
                                args = clear_data[y][x].split(",", 2)[1:]
                                mod = eval(args[1])
                                mod = Weapon.WeaponMod(None, *mod)
                            else:
                                mod = Weapon.WeaponMod(self, "Red dot", [0, 3], "optic",
                                                       [("Spread", "self.weapon.spread[3]", [0.5, 0.5, 0.5])], 100)
                            self.state.items.add(PickUp.ItemWeaponMod(self.app, self.state, self,
                                                                      (x, y), mod))

                    elif clear_data[y][x].split(",")[0] == 'mob':
                        self.state.mobs.add(
                            Mob.Mob(self.app, self.state, self, (self.block_size[0] * x, self.block_size[1] * y)))
                        self.map[y].append(None)

                    elif clear_data[y][x].split(",")[0] == 'NPC':
                        if len(args) > 1:
                            actions = args[1]
                        else:
                            actions = []

                        if len(args) > 2:
                            type = args[2]
                        else:
                            type = "anvil"

                        self.state.npcs.add(
                            NPC.NPC(self.app, self.state, self, (x, y), actions, image=img, type=type))
                        self.map[y].append(None)

                    elif clear_data[y][x].split(",")[0] == "teleport":
                        if len(args) > 1:
                            ttype = args[1]
                        else:
                            ttype = "level"

                        self.state.npcs.add(Teleport.Teleport(self.app, self.state, self, (x, y), ttype, img))
                        self.map[y].append(None)

                    elif clear_data[y][x].split(',')[0] == 'lava':
                        damage = 1
                        collide = True
                        if len(args) > 2 and args[1] != '' and args[2] != '':
                            damage = int(args[1])
                            collide = False
                        elif len(args) > 1 and args[1] != '':
                            damage = int(args[1])
                        self.map[y].append(Blocks.Lava(self.app, self, (x, y), img, damage, collide=collide))

                    elif clear_data[y][x].split(',')[0] == 'stairs':
                        self.state.stairs.add(Blocks.Ladder(self.app, self, (x, y), img))
                        self.map[y].append(None)
                    else:
                        self.map[y].append(None)

                else:
                    self.map[y].append(None)

    def map_move(self, delta_pos):
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                if self.map[row][col]:
                    self.map[row][col].move(delta_pos)

    def return_map(self):
        return self.map

    def delete(self, obj):
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                if self.map[row][col] == obj:
                    self.map[row][col] = None
