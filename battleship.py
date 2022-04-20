# Точи в матрице игрового поля. Для точки указывается
# какому кораблю она принадлежит
# бита ли она
# содержит метод, выдающий отображение точки при выводе: 'О', '■', 'X', 'T'
class Dot:
    ship=None
    hit=None

    def __init__(self, ship=None): # ПРи создании можно указать корабль, но не попадание
        self.ship=ship
        self.hit=False

    def set_ship(self, ship=None):
        self.ship=ship

    def printdot(self):
        if self.ship is None:
            if self.hit :
                return 'T'
            else:
                return '0'
        else:   # там корабль
            if self.hit:
                return 'X'
            else:
                return '■'



    # Для представления корабля на игровой доске напишите класс Ship
# (в конструктор передаём информацию о его положении на доске).

class Ship:
    def __init__(self, place=(0,0)):
        self.place = place

    def set_place(self, place):
        self.place = place

# Другой класс описывает доски, на которых будут размещаться корабли.
# Корабли должны находится на расстоянии минимум одна клетка друг от друга.
# Корабли на доске должны отображаться следующим образом (пример):
# 6 | ■ | ■ | ■ | О | О | О |
# 5 | О | О | О | О | ■ | ■ |
# 4 | О | О | О | О | О | О |
# 3 | ■ | О | ■ | О | ■ | О |
# 2 | О | О | О | О | ■ | О |
# 1 | ■ | О | ■ | О | О | О |
#     a   b   c   d   e   f
# Доска вмещает 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.

class Board:
    def __init__(self):
        self.map=[['O']*6]*6

    def printboard(self):
        print('    1    2    3    4    5    6')
        for r, c in zip(['a','b','c','d','e','f'], range(6)):
            print(r, self.map[c])

############
# Логика игры
# Общий класс для игроков, живого и компьютера
class Player:
    def __init__(self):
        self.myboad=Board()     # своя доска
        self.foeboard=Board()   # доска оппонента




    def ask(self):  #
