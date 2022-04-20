# Точки в матрице игрового поля. Для точки указывается,
# какому кораблю она принадлежит и бита ли она?
# класс содержит метод, выдающий отображение точки при выводе: 'О', '■', 'X', 'T'
class Dot:
    ship=None
    hit=None

    def __init__(self, ship=None): # При создании можно указать корабль, но не попадание в точку
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



class Ship:
    # Для представления корабля на игровой доске напишите класс Ship
    # (в конструктор передаём информацию о его положении на доске).
    def __init__(self, place=None, size=0, dir=None):       # Нужен
        self.place = place

    def set_place(self, place):
        self.place = place

class Board:
    # Другой класс описывает доски, на которых будут размещаться корабли.
    # Корабли должны находится на расстоянии минимум одна клетка друг от друга.
    # Доска вмещает 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
    # Корабли на доске должны отображаться следующим образом (пример):
    # 6 | ■ | ■ | ■ | О | О | О |
    # 5 | О | О | О | О | ■ | ■ |
    # 4 | О | О | О | О | О | О |
    # 3 | ■ | О | ■ | О | ■ | О |
    # 2 | О | О | О | О | ■ | О |
    # 1 | ■ | О | ■ | О | О | О |
    #     a   b   c   d   e   f
    def __init__(self, hiden=False):
        self.map=[['O']*6]*6

    def printboard(self):
        for r, c in zip(range(6,0,-1), range(6)):
            print(r, self.map[c])
        print("    a    b    c    d    e    f")

############
# Логика игры
# Общий класс для живого игрока и компьютера
class Player:
    def __init__(self):
        self.myboad=Board()     # своя доска
        self.foeboard=Board()   # доска оппонента

    def ask(self):  #
        pass

class Ai(Player):
    def ask(self):
        pass

class User(Player):
    def ask(self):
        pass

# Теперь класс хода игры
class Game:
    user=User()             # Пользователь, его ходы и так далее
    user_board=Board()
    ai=Ai()                 # Компьютер
    ai_board=Board(hiden=True)

    def random_board(self, board):
        # Здесь на доске генерится случайное расположение кораблей, начиная с самого большого
        # Корабли накидываются случайным образом, используя метод вставки корабля на доску
        pass

    def greet(self):
        pass

    def loop(self):     # Это цикл хода игры
        pass

    def start(self):
        self.greet()
        self.loop()
