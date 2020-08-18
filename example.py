from pydove import Game

M1 = [[-2, 2, -1], [1, 1, 1], [3, 0, 1]]
M2 = [[3, -1], [-1, 9]]
M3 = [[0, 2, 2], [1, 2, 2], [2, 3, 3], [-1, 4, 4], [-2, 5, 5], [2, 6, 6], [-10, 7, 7]]
M4 = [[10, 0, 7, 4], [2, 6, 4, 7], [5, 2, 3, 8]]
g = Game(M4)
# g.drop_dominated(M4, inplace=True)
# print(g)
# Pydove = g.mixed_values_inequalities()
# print(Pydove)

print( \
    g.game_matrix, "\n",
    g.values(), "\n",
    "saddle_points:", "\n",
    g.saddle_points(), "\n",
    g.mixed_values(), "\n",
    "inneq:", "\n",
)
