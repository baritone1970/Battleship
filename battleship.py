# Классы для игры в морской бой
# Dot - точки игрового поля, отмечают наличие корабля, атаку, отрисовку....
# Ship - размеры и число повреждений корабля
# Board - расстановка и местоположение кораблей, перечень кораблей, отрисовка поля
# User - класс действий игрока
# AI - класс действий компьютера
# Game - класс хода игры

import random

# Сначала займёмся исключениями
# Исключения, связанные с созданием и размещением корабля
class ShipException(Exception):
    def __init__(self, text, data):
        self.text = text
        self.data = data

class BoardException(Exception):
    def __init__(self, text):
        self.text = text

class ShotException(Exception):
    def __init__(self, text):
        self.text = text


######################
# Точки в матрице игрового поля. Для точки указывается,
# какому кораблю она принадлежит и бита ли она?
# класс содержит метод, выдающий отображение точки при выводе: 'О', '■', 'X', 'T'
class Dot:
    ship = None
    hit = False

    def __init__(self, ship=None):  # При создании можно указать корабль, но не попадание в точку
        self.ship = ship
        self.hit = False

    def is_busy(self):  # Занята ли точка кораблём?
        return not (self.ship is None)

    def get_hit(self):  # Был ли выстрел в данную точку?
        return self.hit

    def set_hit(self):  # отметить выстрел в точку и попадание в корабль
        if not self.hit:
            self.hit = True
            if not self.ship is None:
                self.ship.set_hit()  # отмечаем попадания лишь если не было выстрела и там есть корабль

    def set_ship(self, ship):
        if self.is_busy():  # Если там уже корабль, положено вызвать исключение
            raise ShotException("Place is busy")
        else:
            self.ship = ship

    def __str__(self):  # Переопределяем, чтобы печатать точку простейшим способом
        if self.ship is None:
            if self.hit:
                return 'T'
            else:
                return 'O'
        else:  # там корабль
            if self.hit:
                return 'X'
            else:
                return '■'


# Вариант точки для скрытой доски - не печатает корабли
class DotOnHidenBoard(Dot):
    def __str__(self):  # Переопределяем, чтобы печатать точку простейшим способом
        if self.ship is None:
            if self.hit:
                return 'T'
            else:
                return 'O'
        else:  # там корабль
            if self.hit:
                return 'X'
            else:
                return 'O'  # На скрытой доске корабль не показываем


class Ship:
    size = None
    lives = None  # переменная остатка живучести корабля, вычитается при попадании

    # Для создания корабля нам нужен только размер
    def __init__(self, size):  # Нужен
        if 0 < size < 4:
            self.size = size
            self.lives = size
        else:
            raise ShipException("Invalid ship size error", size)

    def set_hit(self):
        if self.lives > 0:
            self.lives -= 1

    def set_place(self, place):  # Думаю, этот метод лучше иметь в классе Board, но посмотрим
        pass


class Board:
    # Класс описывает доски, на которых будут размещаться корабли.
    # Корабли должны находится на расстоянии минимум одна клетка друг от друга.
    # Доска вмещает 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.

    def __init__(self, hidenboard=False):
        random.seed()
        self.map = []  # Будет содержать карту точек кораблей, список строк (списков точек).
        # Номер элемента строки (колонка c) вводится буквой, номер строки r - цифрой
        # Помни, студент: в координате map[r][c] сначала номер строки, потом - номер колонки
        for r in range(6):  # Точки на карте при создании не принадлежат никаким кораблям
            if hidenboard:
                self.map.append([DotOnHidenBoard() for d in range(6)])
            else:
                self.map.append([Dot() for d in range(6)])
        self.free_dots = set()  # Множество свободных для размещения кораблей точек [0-5][0-5]
        for r in range(6):
            for c in range(6):
                self.free_dots.add((r, c))  # self.map[r][c]
        self.ship_list = []  # список кораблей
        for s in [3, 2, 2, 1, 1, 1, 1]:  # список размеров размещаемых кораблей по порядку от 3 до 1
            self.ship_list.append(Ship(s))
        self.error_placement_count=0    # Счётчик числа ошибок размещения, чтобы не зациклиться


    def coord_in_map(self, place):
        # Положение вводится строкой, буква (колонка c) и цифра (ряд r)
        # Защита от неправильного ввода - внешним исключением, но можно вводить и строчные и заглавные буквы
        c = ord(place[0]) - 65  # Если заглавная
        if c > 31:  # Если строчная буква
            c = c - 32
        r = int(place[1]) - 1
        return r, c  # self.map[r][c]

    def clean_around(self, r, c):  # Удаляем из свободных точку под кораблём и воокруг него
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                self.free_dots.discard((r + dr, c + dc))

    def place_ship(self, ship, place, dir):
        # Положение вводится кортежем (строка,столбец), направление - символами 'U', 'R', 'D', 'L'
        r, c = place
        shipdots = []  # Здесь будут точки
        if dir in {'U', 'u'}:
            for d in range(ship.size):
                shipdots.append((r + d, c))
        elif dir in {'R', 'r'}:
            for d in range(ship.size):
                shipdots.append((r, c + d))
        elif dir in {'D', 'd'}:
            for d in range(ship.size):
                shipdots.append((r - d, c))
        elif dir in {'L', 'l'}:
            for d in range(ship.size):
                shipdots.append((r, c - d))
        else:
            raise ShipException("Invalid ship direction error", place)
        # Если исключение выхода из границ, то корабль размещать не надо!
        try:
            for r, c in shipdots:
                # Сначала провоцируем исключение по границам поля и проверяем доступность поля для размещения корабля
                if self.map[r][c].is_busy() or not ((r, c) in self.free_dots):
                    raise ShipException("Здесь корабль разместить не получится!", place)  #
        except IndexError:
            raise ShipException("Попали на точку за пределами поля!", place)
        else:  # Ура, все точки корабля на допустимом месте!
            for r, c in shipdots:
                self.map[r][c].set_ship(ship)  #
                self.clean_around(r, c)  # Удаляем из числа свободных точку под кораблём и воокруг него

    def place_all_ships(self, auto=False):
        for ship in self.ship_list:  # список размеров размещаемых кораблей по размеру от 3 до 1
            done = False
            while not done:
                try:
                    if auto:
                        place=random.choice(tuple(self.free_dots))
                        for dir in ['U', 'R', 'D', 'L']:
                            self.place_ship(ship, place, dir)
                    else:
                        us = input('Введите начальную координату и направление '+str(ship.size)+'-клеточного корабля: ')
                        place = self.coord_in_map(us[:2])  # первые два символа - координата
                        if ship.size > 1:
                            self.place_ship(ship, place, us[2])  # Третий символ ввода - направление
                        else:
                            self.place_ship(ship, place, 'U')  # Одноклеточному кораблю достаточно координаты
                except (IndexError, ShipException) as e:
                    self.error_placement_count += 1
                    if self.error_placement_count > 100:
                        raise BoardException("Что-то не влезают все корабли, устал расставлять.")
                    if True: #not auto:
                        print(e.text, self.error_placement_count, 'ошибок!')
                else:
                    self.printboard()
                    done = True

    def printboard(self):  # Будет использовано при расстановке кораблей.
        for r in range(6, 0, -1):  # Печать по строкам
            print(r, ' | ' + ' | '.join(list(map(str, self.map[r - 1]))) + ' |')
        print("     a   b   c   d   e   f")


############
# Логика игры
class Player:
    # Общий класс для живого игрока и компьютера
    def __init__(self):
        pass

    def ask(self):  #
        pass


class AI(Player):
    # Класс игровой механики компьютера, переопределён ввод точек атаки
    def ask(self):
        pass


class User(Player):
    # Класс игровой механики игрока, переопределён ввод точек атаки
    def ask(self):
        answer = input('Введите номер поля (например, a2): ')


# Теперь класс хода игры
class Game:
    def __init__(self):
        self.user = User()  # Игровая механика пользователя
        self.user_board = Board()  # Доска пользователя
        self.ai = AI()  # Игровая механика компьютера
        self.ai_board = Board(hidenboard=True)
        # self.ai_board.map[2][4].ship=Ship(1)    #TODO

    def random_board(self, board):
        # Здесь на доске генерится случайное расположение кораблей, начиная с самого большого
        # Корабли накидываются случайным образом, используя метод вставки корабля на доску
        pass

    def printboards(self):
        print("          Ваша доска                        Доска противника")
        for r in range(6, 0, -1):  # Печать по строкам
            print(r, ' | ' + ' | '.join(list(map(str, self.user_board.map[r - 1]))) + ' |    #   ',
                  r, ' | ' + ' | '.join(list(map(str, self.ai_board.map[r - 1]))) + ' |')
        print("     a   b   c   d   e   f                a   b   c   d   e   f")

    def greet(self):
        print('''Привет, игрок!
Сейчас мы сыграем в "Морской Бой". Слева будет Ваша доска, справа - доска противника.''')
        self.printboards()
        print('''Координаты вводятся как в шахматах: сначала - буква, потом - цифра, без пробела. 
Например, "e2", "E4" :-)
Сейчас мы расставим ваши корабли. Место указывается так: 
Сначала координата кормы, и сразу без пробела - буква направления, "U", "R", "L" или "D".
Например: "e2u", "E4D". ''')

    def loop(self):  # Это цикл хода игры
        try:
            self.user_board.place_all_ships(auto=True)#
            # self.ai_board.place_all_ships()#auto=True
            self.printboards()
        except BoardException as e:
            self.printboards()
            print(e.text)
        except:
            print('\nЧто-то не получилось у нас. Попробуем в другой раз?\n  Удачи во всех делах и безделье!')

    def start(self):
        self.greet()
        self.loop()
