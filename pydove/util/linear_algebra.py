from sympy import symbols, Matrix, Rel
from sympy.solvers import *


# todo replace solve with the sympy solve_innequality

def convex2_relational_combination(eq1, eq2, eq3, relation):
    """
    Checks if eq3 is Pydove dominated by Pydove convex combination of eq1 and eq2

    if eq3 (==|<=|>=|<|>|!=) λ eq1 + (1 - λ) - eq2

    :param relation: '==' for normal combination, "<=" for rows, ">=" for columns
    :param eq1: First equation
    :param eq2: Second equation
    :param eq3: Third equation and convex combination target
    :return: True or Flase
    """

    x = symbols('λ')
    eq1 = eq1 * x
    eq2 = eq2 * (1 - x)
    sysq = list(map(lambda arg1, arg2: Rel(arg2, sum(arg1), "<="), zip(eq1, eq2), eq3))
    return solve(sysq)



# todo see how to auto plot with matplotlib
# and add to gamematrix
def solve_innequalities(matrix):
    """
    solves game matrixes with equilibrium theorem and innequalities

    :param matrix:
    :return: set of innequalities
    """
    matrix = Matrix(matrix)
    X = symbols('x1:%d' % (matrix.rows + 1))
    matrix = matrix * Matrix([[v] for v in X])
    x_comb = 1 - sum(X[:-1])
    innequalities_matrix = [*map(lambda i: Rel(i.subs(X[-1], x_comb), 1, '<='), matrix)]
    max_u_limit = Rel(sum(X[:-1]), 1, '<=')
    min_l_limit = Rel(sum(X[:-1]), 0, '>=')
    x_all_u_limits = [*map(lambda x_var: Rel(x_var, 1, '<='), X[:-1])]
    x_all_l_limits = [*map(lambda x_var: Rel(x_var, 0, '>='), X[:-1])]
    innequalities_matrix.extend([max_u_limit, min_l_limit, *x_all_u_limits, *x_all_l_limits])
    for var in X[:-1]:
        try:
            innequalities = solve(innequalities_matrix, var)
        except("Cannot solve variable ", var):
            pass
        else:
            return [*innequalities]
    # return empty if there are no solutions
    return []
