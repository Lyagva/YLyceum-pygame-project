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
import PickUp
import PlayerSpawn
import Mob


class Map:
    def __init__(self, app, state, file="maps/1.map"):
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
                        self.map[y].append(Blocks.Block(self.app, self, (x, y), img))

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

                    elif clear_data[y][x].split(",")[0] == 'mob':
                        self.state.mobs.add(
                            Mob.Mob(self.app, self.state, (self.block_size[0] * x, self.block_size[1] * y)))
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
