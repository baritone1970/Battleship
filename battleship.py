# Классы для игры в морской бой
# Dot - точки игрового поля, отмечают наличие корабля, атаку, отрисовку....
# Ship - размеры, число повреждений корабля и скрытость на доске
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


class ShotException(Exception):     # На случай повторного выстрела в точку
    def __init__(self, text):
        self.text = text


######################
# Точки в матрице игрового поля. Для точки указывается,
# какому кораблю она принадлежит и бита ли она?
# класс содержит метод, выдающий отображение точки при выводе: 'О', '■', 'X', 'T'
class Dot:
    def __init__(self, ship=None):  # При создании можно указать корабль, но не попадание в точку
        self.ship = ship
        self.hit = False

    def is_busy(self):  # Занята ли точка кораблём?
        return not (self.ship is None)

    def get_hit(self):  # Был ли выстрел в данную точку?
        return self.hit

    def strike(self):  # сделать выстрел, отметить событие и попадание в корабль
        if not self.hit:
            self.hit = True
            if not self.ship is None:
                self.ship.set_hit()  # отмечаем попадания лишь если не было выстрела и там есть корабль
                return True # Возврат события попадания в точку для пропуска хода оппонентом
        else:
            raise ShotException("Два раза в одну точку стрелять нельзя") # Два раза в одну точку стрелять нельзя

    def set_ship(self, ship):
        if self.is_busy():  # Если там уже корабль, положено вызвать исключение
            raise ShipException("Здесь уже стоит корабль")
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
                if self.ship.hiden:  # Показываем в завивимости от видимости корабля
                    return 'O'
                else:
                    return '■'


class Ship:
    # При создания корабля указывается только размер, и метка показа его на доске
    def __init__(self, size, hiden=False):
        if 0 < size < 4:
            self.size = size
            self.lives = size  # переменная остатка живучести корабля, вычитается при попадании
            self.hiden = hiden
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
        self.hidenboard=hidenboard
        self.reset_board(self.hidenboard)

    def reset_board(self, hidenboard=False):
        self.map = []  # Будет содержать карту точек кораблей, список строк (списков точек).
        # Номер элемента строки (колонка c) вводится буквой, номер строки r - цифрой
        # Помни, студент: в координате map[r][c] сначала номер строки, потом - номер колонки
        for r in range(6):  # Точки на карте при создании не принадлежат никаким кораблям
            self.map.append([Dot() for d in range(6)])
        self.free_dots = set()  # Множество свободных для размещения кораблей точек [0-5][0-5]
        for r in range(6):
            for c in range(6):
                self.free_dots.add((r, c))  # self.map[r][c]
        self.ship_list = []  # список кораблей
        for s in [3, 2, 2, 1, 1, 1, 1]:  # список размеров размещаемых кораблей по порядку от 3 до 1
            self.ship_list.append(Ship(s, hidenboard))  # отмечаем видимость кораблей на доске
        self.error_placement_count = 0  # Счётчик числа ошибок размещения, чтобы не зациклиться

    def coord_in_map(self, place): # трансляция буквенно-цифрового кода координаты в номер элемента map
        # Положение вводится строкой, буква (колонка c) и цифра (ряд r)
        # можно вводить строчные и заглавные буквы
        # Защита от неправильного ввода - внешним исключением.
        c = ord(place[0]) - 65  # Если заглавная
        if c > 31:  # Если строчная буква
            c = c - 32
        r = int(place[1]) - 1
        # self.map[r][c] # Можно использовать для вызова исключения выхода за границу поля
        return r, c

    def clean_around(self, r, c):  # Удаляем из числа свободных точку под кораблём и кругом него
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
            raise ShipException("И в каком направлении расположить корабль?", place)
        # Если исключение выхода из границ, то корабль размещать не надо!
        try:
            for r, c in shipdots:
                # Сначала провоцируем исключение по границам поля и проверяем доступность поля для размещения корабля
                if self.map[r][c].is_busy():
                    raise ShipException("Здесь уже стоит другой корабль.", place)  #
                elif not ((r, c) in self.free_dots):
                    raise ShipException("Здесь корабль задевает другой", place)  #
        except IndexError:
            raise ShipException("Выход за пределы поля!", place)
        else:  # Ура, все точки корабля на допустимом месте!
            for r, c in shipdots:
                self.map[r][c].set_ship(ship)  #
                self.clean_around(r, c)  # Удаляем из числа свободных точку под кораблём и вокруг него

    def place_all_ships(self, auto=False):
        board_done = userauto = False
        while not board_done:  # Много неудач размещения кораблей - доска обнуляется
            try:
                for ship in self.ship_list:  # список размеров размещаемых кораблей по размеру от 3 до 1
                    ship_done = False
                    while not ship_done:
                        try:
                            if auto:
                                place = random.choice(tuple(self.free_dots))
                                dir = random.choice(['U', 'R', 'D', 'L'])
                                self.place_ship(ship, place, dir)
                            else:
                                answer = input('Введите начальную координату и направление ' + str(ship.size) + '-клеточного корабля: ')
                                if answer == 'auto':
                                    auto = userauto = True
                                    raise BoardException("Хорошо, размещу Ваши корабли автоматически")
                                place = self.coord_in_map(answer[:2])  # первые два символа - координата
                                if ship.size > 1:
                                    self.place_ship(ship, place, answer[2])  # Третий символ ввода - направление
                                else:
                                    self.place_ship(ship, place, 'U')  # Одноклеточному кораблю достаточно координаты
                        except (IndexError, ValueError, ShipException) as e:
                            if isinstance(e, ShipException) and not auto:
                                print(e.text)
                            self.error_placement_count += 1
                            if self.error_placement_count > 20:
                                self.error_placement_count = 0
                                raise BoardException("Что-то не получается расставить корабли, очищаю доску, начнём заново.")
                        else:
                            if not auto:
                                self.printboard()  # Только при ручной расстановке
                            ship_done = True
            except BoardException as e:
                if userauto or not auto:
                    print(e.text)
                self.reset_board(self.hidenboard)
            else:
                board_done = True

    def printboard(self):  # Будет использовано при расстановке кораблей.
        for r in range(6, 0, -1):  # Печать по строкам
            print(r, ' | ' + ' | '.join(list(map(str, self.map[r - 1]))) + ' |')
        print("     a   b   c   d   e   f")

    def lives_all(self):
        lives=0
        for s in self.ship_list:
            lives+=s.lives
        return lives



############
# Логика игры
class Player:
    # Общий класс для живого игрока и компьютера
    def __init__(self, own_board, foe_board):
        self.own_board = own_board
        self.foe_board = foe_board
        self.places2hit = set()  # Множество свободных для нанесения удара точек [0-5][0-5]
        for r in range(6):
            for c in range(6):
                self.places2hit.add((r, c))

    def ask(self):  #
        pass

    def strike(self):   # Делается выстрел по координатам, полученным через ask()
        done=False
        while not done:
            try:
                r,c = self.ask()
                hit = self.foe_board.map[r][c].strike()   # Используется метод точки на доске
            except (IndexError, ValueError):
                pass
            except ShotException as e:
                print(e.text)
            else:
                done = True
        return hit


class AI(Player):
    # Класс игровой механики компьютера, переопределён ввод точек атаки
    def ask(self):
        point2hit = random.choice(tuple(self.places2hit))   # Может ли быть прерывание IndexError из-за размера places2hit?
        self.places2hit.discard(point2hit)  # Чтобы не стрелять два раза в одну точку
        return point2hit


class User(Player):
    # Класс игровой механики игрока, переопределён ввод точек атаки
    def ask(self):
        done=False
        while not done:
            try:
                #f = random.choice('abcdef')+random.choice('123456')
                r, c = random.choice(tuple(self.places2hit))
                f='abcdef'[c]+'123456'[r]   # Это чтобы, стреляя по подсказкам, не попадать на уже битые точки ))
                #answer = input('Введите номер поля (например, ' + f + '): ')
                point2hit = self.foe_board.coord_in_map(f)#answer[:2])
            except (IndexError, ValueError):
                pass
            else:
                done=True
                self.places2hit.discard(point2hit)  # Игрок сам должен знать, куда он стрелял, это для подсказок
                return point2hit

# Теперь класс хода игры
class Game:
    def __init__(self):
        random.seed()
        self.user_board = Board()  # Доска пользователя
        self.ai_board = Board(hidenboard=True)  # hidenboard=True # Доска компьютера
        self.user = User(self.user_board, self.ai_board)  # Игровая механика пользователя
        self.ai = AI(self.ai_board, self.user_board)  # Игровая механика компьютера

    def printboards(self):
        print("\n          Ваша доска                        Доска противника")
        for r in range(6, 0, -1):  # Печать по строкам
            print(r, ' | ' + ' | '.join(list(map(str, self.user_board.map[r - 1]))) + ' |    #   ',
                  r, ' | ' + ' | '.join(list(map(str, self.ai_board.map[r - 1]))) + ' |')
        print("     a   b   c   d   e   f                a   b   c   d   e   f")

    def greet(self):
        print('''   Привет, игрок!
Сейчас мы сыграем в "Морской Бой". 
Подождите, я быстренько расставлю корабли противника.....''')
        self.ai_board.place_all_ships(auto=True)  #
        print('''    Готово!
Слева будет Ваша доска, справа - доска противника.
Координаты вводятся как в шахматах: сначала - буква, потом - цифра, без пробела. 
    Например: "e2", "E4" :-)''')
        self.printboards()
        print('''Теперь расставьте свои корабли. Место указывается так: 
Сначала координата кормы, и сразу без пробела - буква направления, "U", "R", "L" или "D".
    Например: "e2u", "E4D". ''')

    def loop(self):  # Это цикл хода игры
        try:
            self.user_board.printboard()     #self.printboards()
            self.user_board.place_all_ships()  # auto=True # TODO - отменить авторазмещение после отработки игровой механики
            #self.printboards()  #TODO - убрать после отработки игровой механики
            game_over = False
            user_pass_now = False   # Переключает ход пользователя или оппонента?
            while not game_over:
                if user_pass_now:
                    #print("ход пользователя")
                    if not self.user.strike():
                        user_pass_now = not user_pass_now
                else:
                    #print("ход ИИ")
                    if not self.ai.strike():
                        user_pass_now = not user_pass_now
                self.printboards()
                #user_pass_now = True   #TODO - для тестирования в режиме ходов только одной из сторон
                #print('AI lives', self.ai_board.lives_all())
                #print('user lives', self.user_board.lives_all())
                if not self.ai_board.lives_all():
                    print("Поздравляем, Вы выиграли!")
                    game_over = True
                elif not self.user_board.lives_all():
                    print("Компьютер пока выиграл. Но в следующий раз постарайтесь победить!")
                    game_over = True
        except KeyboardInterrupt:
            self.printboards()
            print('\nНаскучила игра? До новых встреч!\n  Удачи во всех делах и безделье!')
        except:
            self.printboards()
            print('\nЧто-то не получилось у нас. Попробуем в другой раз?\n  Удачи во всех делах и безделье!')

    def start(self):
        self.greet()
        self.loop()
