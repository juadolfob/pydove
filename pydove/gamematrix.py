import itertools

import sympy as sym
import numpy as np
from pydove.util import *


def _validate_game_matrix(game_matrix):
    is_mxn = all(len(row) == len(game_matrix[0]) for row in game_matrix)
    return is_mxn


class GameMatrix:

    def __init__(self, game_matrix):
        # replace with sym.Matrix validation
        if _validate_game_matrix(game_matrix):
            self.game_matrix = game_matrix

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
    def mixed_values(self):
        A = sym.Matrix(self.game_matrix)
        set = sym.symbols('x1:%d v' % (A.rows + 1))
        e = sym.Matrix([([1] * A.cols) + [0]])
        b = sym.Matrix(([0] * A.rows) + [1])

        M = (A.row_join(sym.Matrix([-1] * A.cols))).col_join(e)
        res = sym.linsolve((M, b), set)
        res = res.args[0]
        return {str(set[i]): res[i] for i in range(len(set))}

    # todo complete
    def mixed_values_inequalities(self):
        A = sym.Matrix(self.game_matrix)
        print(A)

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
