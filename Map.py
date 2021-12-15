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
from pprint import pprint

import pygame as pg

# Импорт классов
import Block

class Map:
    def __init__(self, app, file = "maps/1.map"):
        self.app = app
        self.file = file

        self.map_offset = (0, 0)  # Смещение всей карты в пикселях (К примеру при движении персонажа)
        # К примеру: при (100, 0) начала карты уедет на 100 пикс. ВЛЕВО, как при ходьбе в ПРАВО

        self.map_size = (100, 20)  # Размер карты в блок
        self.block_size = (50, 50)  # Размер блока в пикселях

        # (Вначале y, а потом x)
        self.map = [[Block.Block(self.app, self, (x, y))
                     for x in range(self.map_size[0])]
                    for y in range(self.map_size[1])]

        self.read_file()

    def update(self):
        # Вначале y, а потом x
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                if self.map[row][col]:
                    self.map[row][col].update()

    def render(self):
        # Вначале y, а потом x
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                if self.map[row][col]:
                    self.map[row][col].render()

    def read_file(self):
        self.map = []
        with open(self.file) as file:
            raw_data = file.readlines()
        self.map_size = (int(raw_data[0].split()[0]), int(raw_data[0].split()[1])) # ширина, выоста
        no_spaces_data = ["".join([i for i in line if i != " "]).replace("\n", "")
                          for line in raw_data[1:]] # Очистка от пробелов

        clear_data = [[i for i in line.split(";")]
                          for line in no_spaces_data] # Подводка

        # Тут мы добаляем все элементы
        for y in range(self.map_size[1]):
            self.map.append([])
            for x in range(self.map_size[0]):
                if y < len(clear_data) and x < len(clear_data[y]):
                    # Получение аргументов
                    args = clear_data[y][x].split(",")[1:]
                    if clear_data[y][x].split(",")[0] == "block": # Проверка если это блок
                        if len(args) > 0:
                            img = args[0]
                        else:
                            img = None

                        self.map[y].append(Block.Block(self.app, self, (x, y), img))
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