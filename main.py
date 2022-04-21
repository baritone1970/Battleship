# Суть написанного приложения — игра «Морской бой».
# Интерфейс приложения должен представлять из себя консольное окно с двумя полями 6х6 вида:
#  6 ['O', 'O', 'O', 'O', 'O', 'O']
#  5 ['O', 'O', 'O', 'O', 'O', 'O']
#  4 ['O', 'O', 'O', 'O', 'O', 'O']
#  3 ['O', 'O', 'O', 'O', 'O', 'O']
#  2 ['O', 'O', 'O', 'O', 'O', 'O']
#  1 ['O', 'O', 'O', 'O', 'O', 'O']
#      a   b   c   d   e   f
#
# Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже сходил.
# Для представления корабля на игровой доске напишите класс Ship
# (в конструктор передаём информацию о его положении на доске).
# Опишите класс доски, на которую будут размещаться корабли.
# Корабли должны находится на расстоянии минимум одна клетка друг от друга.
# Корабли на доске должны отображаться следующим образом (пример):
# 6 | ■ | ■ | ■ | О | О | О |
# 5 | О | О | О | О | ■ | ■ |
# 4 | О | О | О | О | О | О |
# 3 | ■ | О | ■ | О | ■ | О |
# 2 | О | О | О | О | ■ | О |
# 1 | ■ | О | ■ | О | О | О |
#     a   b   c   d   e   f
#
# На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей:
# 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
# Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение.
# 6 | X | X | X | О | О | О |
# 5 | О | О | О | О | X | X |
# 4 | О | T | О | О | О | О |
# 3 | ■ | О | ■ | О | ■ | О |
# 2 | О | О | О | О | ■ | О |
# 1 | ■ | О | ■ | О | О | О |
#     a   b   c   d   e   f
#
# В случае, если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.
# Буквой X помечаются подбитые корабли, буквой T — промахи.
#
# Побеждает тот, кто быстрее всех разгромит корабли противника.

from battleship import *

if __name__ == '__main__':

    new_game=Game()
    new_game.start()

