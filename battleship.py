# Сначала займёмся исключениями
# Исключения, связанные с созданием и размещением корабля
class ShipException(Exception):
    def __init__(self, text, num):
        self.text = text
        self.num = num


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
        self.map = []  # Будет содержать карту точек кораблей, список строк (списков точек).
        # Номер элемента строки (колонка c) вводится буквой, номер строки r - цифрой
        # Помни, студент: в координате map[r][c] сначала номер строки, потом - номер колонки
        for r in range(6):  # Точки на карте при создании не принадлежат никаким кораблям
            if hidenboard:
                self.map.append([DotOnHidenBoard() for d in range(6)])
            else:
                self.map.append([Dot() for d in range(6)])
        self.free_dots = set()  # Множество свободных точек, используется лишь для ускорения размещения кораблей
        for r in range(6):  # Заполняем множество свободных для размещения кораблей точек [0-5][0-5]
            for c in range(6):
                self.free_dots.add((r, c))  # self.map[r][c]
        self.ship_list = []  # список кораблей
        for s in [1, 1]:  # список размеров размещаемых кораблей по порядку от 3 до 1
            self.ship_list.append(Ship(s))

    def coord_in_map(self, place):
        # Положение вводится строкой, буква (колонка c) и цифра (ряд r)
        # Защита от неправильного ввода - внешним исключением, но можно вводить и строчные и заглавные буквы
        c = ord(place[0]) - 65  # Если заглавная
        if c > 31:  # Если строчная буква
            c = c - 32
        r = int(place[1]) - 1
        return r, c  # self.map[r][c]

    def place_ship(self, ship, place, dir):
        # Положение вводится строкой, буква и цифра, направление - символами 'U', 'R', 'D', 'L'
        r, c = place
        self.map[r][c].set_ship(ship)  # пока никаких проверок.
        for dr in [-1, 0, 1]:       # Удаляем из свободных точку под кораблём и воокруг него
            for dc in [-1, 0, 1]:
                self.free_dots.discard((r + dr, c + dc))
        print(self.free_dots)

    def place_all_ships(self, auto=False):
        for ship in self.ship_list:  # список размеров размещаемых кораблей по порядку от 3 до 1
            done = False
            while not done:
                try:
                    place = self.coord_in_map(input('Введите координаты корабля: '))
                    self.place_ship(ship, place, 'U')
                except ShipException:
                    print('Сюда не помещается')
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


class Ai(Player):
    # Класс игровой механики игрока, переопределён ввод точек атаки
    def ask(self):
        pass


class User(Player):
    # Класс игровой механики компьютера, переопределён ввод точек атаки
    def ask(self):
        answer = input('Введите номер поля (например, a2): ')


# Теперь класс хода игры
class Game:
    def __init__(self):
        self.user = User()  # Игровая механика пользователя
        self.user_board = Board()  # Доска пользователя
        self.ai = Ai()  # Игровая механика компьютера
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
        print('''Сейчас мы расставим ваши корабли. Координаты вводятся как в шахматах: 
сначала - буква, потом - цифра, без пробела. Например, "e2", "e4" :-)''')
        self.user_board.place_all_ships()
        # self.ai_board.map[2][4].hit=True
        self.printboards()

    def loop(self):  # Это цикл хода игры
        pass

    def start(self):
        self.greet()
        self.loop()
