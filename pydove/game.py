from collections import Iterable

from pydove import GameMatrix


def _validate_strategy(strategy_len, strategy):
    has_regular_Iterables = all(strategy_len(row) == strategy_len(strategy[0]) for row in strategy)
    return has_regular_Iterables


class Game(GameMatrix):
    """

    """
    def __init__(self, game_matrix, strategy=None):
        GameMatrix.__init__(self, game_matrix)
        if strategy:
            self.strategy = self._normalize_strategy(strategy)

    def __repr__(self):
        return self.game_matrix.__repr__()

    def __str__(self):
        return "Game(%s)" % self.game_matrix.__str__()

    def _normalize_strategy(self, strategy):
        empty_s = [0] * len(strategy)
        for s in range(len(strategy)):
            if isinstance(s, int):
                int_s = strategy[s]
                strategy[s] = empty_s[:]
                strategy[s][int_s] = 1
            elif isinstance(s, Iterable):
                if not len(s) == len(strategy[s]):
                    raise Exception("")
                if not self.has_mixed_strategies:
                    self.has_mixed_strategies = True

    def dominated_strategy(self):
        pass

    def game_type(self):
        pass

    def detail(self):
        return str(self.values()) + "\n" + str(self.mixed_values())

    def pure_strategies(self):
        pass

    def best_response(self):
        pass
