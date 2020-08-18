import itertools

import sympy as sym
from numpy import array

from pydove.util import *


def _validate_game_matrix(game_matrix):
    is_mxn = all(len(row) == len(game_matrix[0]) for row in game_matrix)
    return is_mxn


class GameMatrix:
    """
    Game matrix


    """

    def __init__(self, game_matrix):
        # replace with sym.Matrix validation
        self.game_matrix = array(game_matrix)
        self.rows, self.cols = self.game_matrix.shape
        if self.rows == self.cols:
            pass

    def __repr__(self):
        return str(self.game_matrix)

    def __str__(self):
        # if self.rows == 0 or self.cols == 0:
        #    return 'GameMatrix(%s, %s, [])' % str(self._game_matrix)
        return "GameMatrix(%s)" % str(self.game_matrix)

    def values(self):
        vu = max([min(row) for row in self.game_matrix])
        vl = min([max(column) for column in np.transpose(self.game_matrix)])
        return {"vl": vl, "vu": vu}

    # saddle points, Nash equilibrium, or optimal strategies
    # todo return with its respective optmal strategies
    # separate mixed and pure optimal

    def saddle_points(self):
        v_key = (lambda t: t[1])

        i_vl = [(i, min(row)) for i, row in enumerate(self.game_matrix)]
        x_max = max(i_vl, key=v_key)[1]
        i_vl = [v for v in i_vl if v[1] == x_max]

        i_vu = [(i, max(col)) for i, col in enumerate(np.transpose(self.game_matrix))]
        y_min = min(i_vu, key=v_key)[1]
        i_vu = [v for v in i_vu if v[1] == y_min]

        i_vl = [i[0] for i in i_vl]
        i_vu = [i[0] for i in i_vu]

        return [*itertools.product(i_vl, i_vu)]

    # todo delete redundant (repeated) pure strategies
    # todo return strategies for all players
    @staticmethod
    def zero_fill_square(arr):
        """

        :param arr:
        :return:
        """
        rows, cols = arr.shape
        b = np.zeros((cols, cols),object)
        if rows >= cols:
            b[:, :cols - rows] = arr
            return b
        b[:rows - cols, :] = arr
        return b

    def mixed_values(self):
        """

        :return:
        """

        var_set = sym.symbols('x1:%d v' % (self.cols + 1))
        var_row = array([([1] * self.cols) + [0]])
        v_column = array([[-1]] * self.rows)

        B_side = array(([[0]] * self.rows) + [[1]])
        M = np.append(self.game_matrix, v_column, axis=1)
        M = np.append(M, var_row, axis=0)
        B_side = Matrix(B_side)

        print(M)

        M = np.append(M, B_side, axis=1)
        if self.rows != self.cols:
            m_row, m_col = M.shape
            #todo fix this
            if m_row > m_col:
                for i in range(m_row - m_col+1):
                    print("NOT LIKE THIS")
                    M = np.append(M, [M[-1]], axis=0)
            else:
                for i in range(m_col-m_row-1):
                    print(M[-1])
                    M = np.append(M, [M[-1]], axis=0)

        print(M)

        print(B_side, "\n", M)
        res = sym.linsolve(Matrix(M), var_set)
        res = res.args[0]
        return {str(var_set[i]): res[i] for i in range(len(var_set))}

    # todo complete
    def mixed_values_inequalities(self):
        pass

    def drop_dominated(self=None, game_matrix=None, inplace=False):
        if self:
            game_matrix = self.game_matrix
        A_matrix = game_matrix
        while A_matrix:
            A_matrix = GameMatrix.drop_dominated_rows(game_matrix=A_matrix)
            A_matrix = GameMatrix.drop_dominated_columns(game_matrix=A_matrix)
            if game_matrix == A_matrix:
                break
            game_matrix = A_matrix
        if inplace:
            self.game_matrix = game_matrix
        return self

    @staticmethod
    def _drop_on_innequality(game_matrix, sign):
        A = []

        for i1 in range(len(game_matrix)):
            is_candidate = True
            for i2 in [i2 for i2 in range(len(game_matrix)) if i2 != i1]:
                if all([comp2(x1, x2, sign) for x1, x2 in (zip(game_matrix[i1], game_matrix[i2]))]):
                    is_candidate = False
                    break
            if is_candidate:
                A.append(game_matrix[i1])
        return A

    def drop_dominated_rows(self=None, game_matrix=None, inplace=False):
        if self:
            game_matrix = self.game_matrix
        game_matrix = GameMatrix._drop_on_innequality(game_matrix, "<")
        if inplace:
            self.game_matrix = game_matrix
            return self
        return game_matrix

    def drop_dominated_columns(self=None, game_matrix=None, inplace=False):
        if self:
            game_matrix = self.game_matrix
        game_matrix = np.transpose(GameMatrix._drop_on_innequality(np.transpose(game_matrix).tolist(), ">")).tolist()
        if inplace:
            self.game_matrix = game_matrix
            return self
        return game_matrix

    def detail(self):
        return str(self.values()) + "\n" + str(self.mixed_values())

    def pure_strategies(self):
        pass

    def best_response(self):
        pass
