# Класс карты. Ну тут храниться матрица блоков
"""
Формат карты предлагаю использовать такой:
    Матрица, где одна строчка - одна строчка массива, а все элементы разделены ";".
    Все пробелы просто будем очищать.

    Каждый элемент:
        <Тип (блок, сущность и т.д.)>,<Текстура>,<Чё нибудь ещё>;

        Пример блока:
            block,1.png;

Пример матрицы:

block,1.png;block,1.png;block,1.png;block,1.png
block,1.png;           ;           ;block,1.png
block,1.png;           ;           ;block,1.png
block,1.png;           ;           ;block,1.png
block,1.png;block,1.png;block,1.png;block,1.png
"""


# Импорт библиотек
import pygame as pg

# Импорт классов
import Block

class Map:
    def __init__(self, app):
        self.app = app

        self.map_offset = (0, 0)  # Смещение всей карты в пикселях (К примеру при движении персонажа)
        # К примеру: при (100, 0) начала карты уедет на 100 пикс. ВЛЕВО, как при ходьбе в ПРАВО

        self.map_size = (100, 20)  # Размер карты в блок
        self.block_size = (50, 50)  # Размер блока в пикселях

        # (Вначале y, а потом x)
        self.map = [[Block.Block(self.app, self, (x, y))
                     for x in range(self.map_size[0])]
                    for y in range(self.map_size[1])]

    def update(self):
        # Вначале y, а потом x
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                self.map[row][col].update()

    def render(self):
        # Вначале y, а потом x
        for row in range(self.map_size[1]):
            for col in range(self.map_size[0]):
                self.map[row][col].render()