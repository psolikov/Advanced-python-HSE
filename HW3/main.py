import numpy as np


class MatrixError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Matrix:
    def __init__(self, matrix: list[list]):
        self.validate_mat(matrix)
        self.mat = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])

    def get_mat(self):
        return self.mat

    @staticmethod
    def validate_mat(matrix):
        m = len(matrix[0])
        for i, row in enumerate(matrix):
            if len(row) != m:
                raise MatrixError(f"Matrix dimension inconsistency " +
                                  f"at row {i}: expected {m} but got {len(row)}.")
            for item in row:
                try:
                    float(item)
                except:
                    raise MatrixError(f"Got nonnumeric item: {item}")

    def __add__(self, add_mat_obj):
        add_mat = add_mat_obj.get_mat()
        self.validate_mat(add_mat)
        if len(add_mat) != self.n:
            raise MatrixError(f"Matrix n dim is {len(add_mat)} but should be {self.n}.")
        if len(add_mat[0]) != self.m:
            raise MatrixError(f"Matrix n dim is {len(add_mat[0])} but should be {self.m}.")

        new_rows = []
        for i, (row_a, row_b) in enumerate(zip(self.mat, add_mat)):
            new_row = []
            for item_a, item_b in zip(row_a, row_b):
                new_row.append(item_a + item_b)
            new_rows.append(new_row)

        return Matrix(new_rows)

    def __mul__(self, other):
        other_mat = other.get_mat()
        self.validate_mat(other_mat)
        if len(other_mat) != self.n:
            raise MatrixError(f"Matrix n dim is {len(other_mat)} but should be {self.n}.")
        if len(other_mat[0]) != self.m:
            raise MatrixError(f"Matrix n dim is {len(other_mat[0])} but should be {self.m}.")

        new_rows = []
        for i, (row_a, row_b) in enumerate(zip(self.mat, other_mat)):
            new_row = []
            for item_a, item_b in zip(row_a, row_b):
                new_row.append(item_a * item_b)
            new_rows.append(new_row)

        return Matrix(new_rows)

    def __matmul__(self, other):
        other_mat = other.get_mat()
        self.validate_mat(other_mat)
        if len(other_mat) != self.m:
            raise MatrixError(f"Matrix n dim is {len(other_mat)} but should be {self.m}.")

        new_rows = []
        for row in self.mat:
            new_row = []
            for i in range(len(other_mat[0])):
                other_row = []
                for j in range(len(other_mat)):
                    other_row.append(other_mat[j][i])
                new_row.append(sum([x * y for x, y in zip(row, other_row)]))
            new_rows.append(new_row)

        return Matrix(new_rows)

    def __hash__(self):
        return sum([sum(row) for row in self.mat])

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for row in self.mat:
                for item in row:
                    f.write(f"{item} ")
                f.write("\n")


class MixinMatrixBase:
    def __init__(self, value):
        self.value = np.asarray(value)


def matrix_to_file(mat_obj: MixinMatrixBase, filename):
    with open(filename, "w") as f:
        for row in mat_obj.value:
            for item in row:
                f.write(f"{item} ")
            f.write("\n")


def matrix_to_str(mat_obj: MixinMatrixBase):
    lst = []
    for row in mat_obj.value:
        for item in row:
            lst.append(f"{item} ")
        lst.append("\n")
    return "".join(lst)


class MatrixSaveToFileMixin:
    def save_to_file(self, filename):
        matrix_to_file(self, filename)


class MatrixToStrMixin:
    def __str__(self):
        matrix_to_str(self)


class MixinMatrix(MixinMatrixBase, np.lib.mixins.NDArrayOperatorsMixin, MatrixSaveToFileMixin, MatrixToStrMixin):
    def __init__(self, value):
        super().__init__(value)

    # One might also consider adding the built-in list type to this
    # list, to support operations like np.add(array_like, list)
    # _HANDLED_TYPES = (np.ndarray, None)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, (np.ndarray, MixinMatrix,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, MixinMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, MixinMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.value)


if __name__ == '__main__':
    np.random.seed(0)
    # mat_a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    # mat_b = [[1, 2], [3, 4], [5, 6], [7, 8]]
    # a = Matrix(mat_a)
    # b = Matrix(mat_b)
    # c = a @ b
    # print(c.get_mat())
    #
    # #####
    #
    # mat_a = np.random.randint(0, 10, (10, 10))
    # mat_b = np.random.randint(0, 10, (10, 10))
    # a = Matrix(list(mat_a))
    # b = Matrix(list(mat_b))
    # (a + b).save_to_file("matrix+.txt")
    # (a * b).save_to_file("matrix*.txt")
    # (a @ b).save_to_file("matrix@.txt")
    #
    # #####
    #
    # mat_a = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    # mat_c = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
    # mat_b = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    # a = Matrix(list(mat_a))
    # a.save_to_file("A.txt")
    # b = Matrix(list(mat_b))
    # b.save_to_file("B.txt")
    # c = Matrix(list(mat_c))
    # c.save_to_file("C.txt")
    # d = Matrix(list(mat_b))
    # d.save_to_file("D.txt")
    #
    # print((a @ b).__hash__())
    # (a @ b).save_to_file("AB.txt")
    # print((c @ d).__hash__())
    # (c @ d).save_to_file("CD.txt")
    #
    # with open("artifacts/hard/hash.txt", "w") as f:
    #     f.write(str((a @ b).__hash__()))
    #

    ####

    mat_a = np.random.randint(0, 10, (10, 10))
    mat_b = np.random.randint(0, 10, (10, 10))
    a = MixinMatrix(list(mat_a))
    b = MixinMatrix(list(mat_b))
    (a + b).save_to_file("matrix+.txt")
    (a * b).save_to_file("matrix*.txt")
    (a @ b).save_to_file("matrix@.txt")
