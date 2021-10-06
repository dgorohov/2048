from functools import reduce
from math import floor
from random import randint, random, seed


def reducer(a, b):
    res_a = a
    extra_b = 0

    a_0 = a[len(a) - 2] if len(a) > 1 else 0
    a_1 = a[len(a) - 1]

    if len(b) == 1:
        b += [0]

    if a_0 == a_1:
        res_a = [a_0 + a_1]
    else:
        extra_b = a_1

    if extra_b == b[0]:
        res_a = res_a[:-1]
        b[0] = extra_b + b[0]
        res_b = b + [0]
    else:
        res_b = b
        if b[0] == b[1]:
            res_b = [b[0] + b[1], 0]

    return [*res_a, *res_b]


class Logic:
    solutions_available = (1, 1)

    def __init__(self, rows=4, columns=4, matrix=None):
        self.__rows = rows
        self.__columns = columns
        if matrix is None:
            self.__matrix = self.__generate_matrix()
            for _ in range(floor(rows / 2)):
                self.add_new()
        else:
            self.__matrix = matrix

    @property
    def matrix(self):
        return self.__matrix

    @staticmethod
    def filter_not_null(items):
        return list(filter(lambda x: x > 0, items))

    @staticmethod
    def filter_end_state(items):
        return list(filter(lambda x: x >= 2048, items))

    def add_new(self) -> bool:
        seed()
        positions = self.positions_available()
        if len(positions) == 0:
            if self.check_rows() is False:
                return self.check_columns()
            return True
        position_index = randint(0, len(positions) - 1)
        probability_of_2 = 0.9
        self.__matrix[positions[position_index][0]][
            positions[position_index][1]] = 2 if random() < probability_of_2 else 4
        return True

    def positions_available(self) -> [()]:
        positions = []
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.__matrix[row][column] == 0:
                    positions.append((row, column))
        return positions

    def __generate_matrix(self):
        return [[0 for _ in range(self.__columns)] for _ in range(self.__rows)]

    def turn_up(self):
        return self.turn_column(-1)

    def turn_down(self):
        return self.turn_column()

    def turn_column(self, direction=1):
        done = self.shift_columns(direction)
        avail = self.check_columns()
        if done:
            return avail, done
        return self.check_rows(), False

    def turn_left(self):
        return self.turn_row(-1)

    def turn_right(self):
        return self.turn_row()

    def turn_row(self, direction=1):
        done = self.shift_rows(direction)
        avail = self.check_rows()
        if done:
            return avail, done
        return self.check_columns(), False

    def check_rows(self):
        for row in range(self.__rows):
            rows = self.filter_not_null(self.__matrix[row])
            if len(rows) != self.__rows:
                return True
            for index in range(len(rows) - 1):
                if rows[index] == rows[index + 1]:
                    return True
        return False

    def check_columns(self):
        for column in range(self.__columns):
            columns = [self.__matrix[row][column] for row in range(0, self.__rows)]
            columns = self.filter_not_null(columns)
            if len(columns) != self.__columns:
                return True
            for index in range(len(columns) - 1):
                if columns[index] == columns[index + 1]:
                    return True
        return False

    def shift_columns(self, direction=1):
        for column in range(0, self.__columns):
            rows = [self.__matrix[row][column] for row in range(0, self.__rows)]
            final = self.filter_end_state(rows)
            if len(final) > 0:
                return True
            self.replace_rows(column, self.squeeze(rows, direction))
        return False

    def replace_columns(self, row, values):
        for column in range(0, len(values)):
            self.__matrix[row][column] = values[column]

    def shift_rows(self, direction=1):
        for row in range(0, self.__rows):
            columns = [self.__matrix[row][column] for column in range(0, self.__columns)]
            final = self.filter_end_state(columns)
            if len(final) > 0:
                return True
            self.replace_columns(row, self.squeeze(columns, direction))
        return False

    def replace_rows(self, column, values):
        for row in range(0, len(values)):
            self.__matrix[row][column] = values[row]

    def squeeze(self, values, direction=1):
        list_values = self.filter_not_null(values)

        def fold(vals):
            if not vals:
                return vals
            if len(vals) == 1:
                res = reducer(vals[0], [-1])
            else:
                res = reduce(reducer, vals if direction == -1 else vals[::-1])
            res = self.filter_not_null(res)
            return res if direction == -1 else res[::-1]

        if direction == 1:
            list_values = list_values[::-1]

        chunks = [
            list_values[max(0, x - 2 * (1 if direction == 1 else 0)):x + 2 * (1 if direction == -1 else 0)]
            for x in range(
                len(list_values) if direction == 1 else 0,
                0 if direction == 1 else len(list_values),
                2 * (direction * -1)
            )]

        chunks = fold(chunks)

        if direction == -1:
            chunks += [0] * (len(values) - len(chunks))
        else:
            chunks = [0] * (len(values) - len(chunks)) + chunks
        return chunks
