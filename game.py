import numpy as np
import sympy as sym


def _validate_game_matrix(game_matrix):
    is_mxn = all(len(row) == len(game_matrix[0]) for row in game_matrix)
    return is_mxn


def _validate_strategy(len, strategy):
    has_regular_Iterables = all(len(row) == len(strategy[0]) for row in strategy)
    return has_regular_Iterables


class game:

    def __init__(self, game_matrix, strategy=None):
        # not necessary maybe
        if _validate_game_matrix(game_matrix):
            self.game_matrix = game_matrix
        if strategy:
            self.strategy = self._normalize_strategy(strategy)

    def _normalize_strategy(self, strategy):
        empty_s = [0] * len(strategy)
        for s in range(len(strategy)):
            if isinstance(s, int):
                int_s = strategy[s]
                strategy[s] = empty_s[:]
                strategy[s][int_s] = 1
            elif isinstance(s, list):
                if not len(s) == len(strategy[s]):
                    raise Exception("")
                if not self.has_mixed_strategies:
                    self.has_mixed_strategies = True

    def dominated_strategy(self):
        pass

    def game_type(self):
        pass

    # saddle points, Nash equilibrium, or optimal strategies
    def optimal_strategies(self):
        pass

    def values(self):
        vu = min([max(row) for row in self.game_matrix])
        vl = max([min(column) for column in np.transpose(self.game_matrix)])
        return {"vl":vl, "vu":vu}

    def mixed_values(self):
        A = sym.Matrix(self.game_matrix)
        set = sym.symbols('x1:%d v' % (A.rows + 1))
        e = sym.Matrix([([1] * A.cols ) + [0]])
        b = sym.Matrix(([0] * A.rows ) + [1])

        M = (A.row_join(sym.Matrix([-1]*A.cols))).col_join(e)
        res = sym.linsolve((M,b),set)
        res = res.args[0]
        print(res, "  ", type(res))
        return {str(set[i]):res[i] for i in range(len(set))}

    def detail(self):
        return str(self.values())+"\n"+str(self.mixed_values())

    def pure_strategies(self):
        pass

    def best_response(self):
        pass


# p 27
M1 = [[1, -1, 1], [-1, 1, -1], [1, -1, 1]]
M2 = [[3,-1], [-1,9]]
g = game(M2)

print(g.detail())