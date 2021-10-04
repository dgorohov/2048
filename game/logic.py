from functools import reduce
from random import randrange, choices, sample


class Logic:
    def __init__(self, rows=4, columns=4, fill_factor=5, pow_limit=11):
        self.__rows = rows
        self.__columns = columns
        self.__pow_limit = pow_limit
        self.__matrix = self.__generate_matrix(fill_factor=fill_factor)

    @property
    def matrix(self):
        return self.__matrix

    def __generate_matrix(self, fill_factor=8, max_generated_pow=5):
        total_count = self.__rows * self.__columns
        pow_pool = list(map(lambda x: 2 ** x, choices(
            [randrange(1, max_generated_pow + 1) for _ in range(fill_factor)],
            weights=[randrange(1, 10) for _ in range(fill_factor)],
            k=fill_factor
        )))
        values = sample(pow_pool + [0] * (total_count - fill_factor), total_count)
        return [
            [values[x * self.__columns + y] for x in range(self.__columns)] for y in range(self.__rows)
        ]

    def turn_up(self):
        self.shift_columns(-1)

    def turn_down(self):
        self.shift_columns()

    def turn_left(self):
        self.shift_rows(-1)

    def turn_right(self):
        self.shift_rows()

    def shift_columns(self, direction=1):
        for column in range(0, self.__columns):
            rows = [self.__matrix[row][column] for row in range(0, self.__rows)]
            self.replace_rows(column, self.squeeze(rows, direction))

    def replace_columns(self, row, values):
        for column in range(0, len(values)):
            self.__matrix[row][column] = values[column]

    def shift_rows(self, direction=1):
        for row in range(0, self.__rows):
            columns = [self.__matrix[row][column] for column in range(0, self.__columns)]
            self.replace_columns(row, self.squeeze(columns, direction))

    def replace_rows(self, column, values):
        for row in range(0, len(values)):
            self.__matrix[row][column] = values[row]

    def squeeze(self, values, direction=1):
        list_values = list(filter(lambda x: x != 0, values))

        if direction == 1:
            list_values = list_values[::-1]

        chunks = [
            list_values[max(0, x - 2 * (1 if direction == 1 else 0)):x + 2 * (1 if direction == -1 else 0)]
            for x in range(
                len(list_values) if direction == 1 else 0,
                0 if direction == 1 else len(list_values),
                2 * (direction * -1)
            )]

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

        def fold(vals):
            if not vals:
                return vals
            if len(vals) == 1:
                res = reducer(vals[0], [-1])
            else:
                res = reduce(reducer, vals if direction == -1 else vals[::-1])
            res = list(filter(lambda x: x > 0, res))
            return res if direction == -1 else res[::-1]

        chunks = fold(chunks)

        if direction == -1:
            chunks += [0] * (len(values) - len(chunks))
        else:
            chunks = [0] * (len(values) - len(chunks)) + chunks
        return chunks
