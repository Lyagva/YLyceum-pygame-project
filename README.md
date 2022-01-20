# Пояснительная записка
### Название проекта
    Lambda-13
### Авторы проекта
    Бадзгарадзе Владимир
    Дубров Артём
## Описание идеи
    2д игра с видом сбоку. События происходят в секретных лабораториях, 
    через которые главному герою (в дальнейшем гг) придётся пройти. 
    Уровни разделены на секторы. По ходу прохождения игрок находит всё более 
    совершенное оружие и модификации, но также встречает всё более сильных врагов.

    Сеттинг - будущее.
    Локации - секретные лаборатории.
    Жанр - 2д-экшен-шутер-платформер-видом_сбоку.
## Описание реализации
    Стиль кода - ООП.
    Классы
        За окна в игре отвечают файлы в папке states а в main файле 
        происходит их update и render в зависимости от выбранного окна.
        так-же существует много классов для самого процесса игры наиболее 
        важные ил них это Camera, Player, Map, Mob, Weapon с говорящими названиями
        так же в большинстве классов существуют 2 метода update и render 
        отвечающие за обновление и отрисовку
        

    Интересные приёмы
        1) передачи экземпляров классов 
        2) еще один интересный приём используется в классе кнопки: 
            что бы кнопка работала она должна изменять 
            некоторые переменные при передача параметров 
            изменения мы передаём функцию 
            которая изменяет какую-либо переменную без () 
            а позже когда кнопка нажата
            мы вызываем эту функцию добавляя ()
        3) востановление сохранений происходить с помошью функции exec

## Описание технологий
    Технологии проекта:
        В проекте использовались текстовые файлы для сохранений и загрузки элементов 
        к примеру в Map
        и огромный функционал модуля pygame
        коллайды - во многих местах к примеру в Player
        анимация - пока только в Danger_Block
        уровни хрвнятся в папке maps 
        подсчёт результатов происходит при переходе в телепорт на следующую локацию
        
        
    Библиотеки: pygame
                imghdr
                os
                math
                random
                datetime
                time
### Техничесоке описание
    Для установки необъодимо прописать pip install -r requirements.txt
    Главный файл, который надо запускать - Main.py
