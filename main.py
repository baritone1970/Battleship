# Суть написанного приложения — игра «Морской бой».
# Интерфейс приложения должен представлять из себя консольное окно с двумя полями 6х6 вида:
#    | 1 | 2 | 3 | 4 | 5 | 6 |
#  1 | О | О | О | О | О | О |
#  2 | О | О | О | О | О | О |
#  3 | О | О | О | О | О | О |
#  4 | О | О | О | О | О | О |
#  5 | О | О | О | О | О | О |
#  6 | О | О | О | О | О | О |
#
# Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже сходил.
# Для представления корабля на игровой доске напишите класс Ship
# (в конструктор передаём информацию о его положении на доске).
# Опишите класс доски, на которую будут размещаться корабли.
# Корабли должны находится на расстоянии минимум одна клетка друг от друга.
# Корабли на доске должны отображаться следующим образом (пример):
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | ■ | ■ | ■ | О | О | О |
# 2 | О | О | О | О | ■ | ■ |
# 3 | О | О | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |
#
# На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей:
# 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
# Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение.
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | О | X | X |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |
#
# В случае, если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.
# Буквой X помечаются подбитые корабли, буквой T — промахи.
#
# Побеждает тот, кто быстрее всех разгромит корабли противника.

if __name__ == '__main__':
    print('PyCharm')
