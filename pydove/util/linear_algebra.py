from sympy import symbols, Eq, Matrix, Rel
from sympy.core import relational
from sympy.solvers import *

from sympy.solvers.inequalities import solve_rational_inequalities, solve_poly_inequalities, solve_poly_inequality


# todo
def convex_combination(*equations):
    pass


# equilibrium theorem
y1, y2, y3 = symbols('y1 y2 y3')
x, y, z = symbols('x y z')
a = solve((-y1 + 3 * y2 < 2,
           2 * y1 - y2 < 1,
           Eq(y1 + y2 < 1, 1)),
          y1)

g = [[-2, 2, -1],
     [1, 1, 1],
     [3, 0, 1]]

#todo see how to auto plot with matplotlib
#and add to gamematrix
def solve_innequalities(matrix):
    """


    :param matrix:
    :return:
    """
    matrix = Matrix(matrix)
    X = symbols('x1:%d' % (matrix.rows + 1))
    matrix = matrix * Matrix([[v] for v in X])
    x_comb = 1 - sum(X[:-1])
    innequalities_matrix = [*map(lambda i: Rel(i.subs(X[-1], x_comb), 1, '<='), matrix)]
    x_u_limit = Rel(sum(X[:-1]), 1, '<=')
    x_l_limit = Rel(sum(X[:-1]), 0, '>=')
    x_all_u_limits = [*map(lambda x_var: Rel(x_var, 1, '<='), X[:-1])]
    x_all_l_limits = [*map(lambda x_var: Rel(x_var, 0, '>='), X[:-1])]
    innequalities_matrix.extend([x_u_limit, x_l_limit, *x_all_u_limits, *x_all_l_limits])
    res = [solve(innequalities_matrix, var) for var in X[:-1]]
    print(innequalities_matrix)
    for i in range(len(res)):
        print(res[i], "\n")


solve_innequalities(g)
