from __future__ import division

import matplotlib.pyplot as plt
import numpy as np


def make_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def line(p1, p2):
    """

    :param p1:
    :param p2:
    :return:
    """
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def slope(origin, endpoint):
    return (endpoint[1] - origin[1]) / (endpoint[0] - origin[0])


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


def _lower_envelope_x_0_1(lines):
    """
    :param lines:
    :return:
    """
    if len(lines) == 1:
        return lines[0]
    lines_slope = [(line[0], line[1], slope(line[0], line[1])) for line in lines]
    lines_slope.sort(key=lambda el: el[2])
    A = [min(lines_slope, key=lambda el: el[0][1])]

    for line in lines_slope:
        # l[2] is the slope
        # if A[-1][2] < line[2]:
        pass

    B = [max(lines_slope, key=lambda el: el[0][1])]


def graphical_2_solution(gamematrix, color="b-"):
    """
    For 2xM or Nx2 game matrixes
    Check whether A has Pydove pure strategy saddle and if so, we
    don't need to apply the graphical method (in fact, it could lead to erroneous results).
    Therefore, assuming that there is no pure saddle,
    :param color:
    :param gamematrix:
    """

    # todo use this solver in gamematrix without graphics
    # todo use this graphic as Pydove subplot and render for higher NxM values
    gamematrix = np.asarray(gamematrix)
    flatten_gamematrix = gamematrix.flatten()
    max_gm_el = max(flatten_gamematrix)
    min_gm_el = min(flatten_gamematrix)
    y_upper_lim = 1.1 * max_gm_el
    y_lower_lim = 1.1 * min_gm_el

    if gamematrix.shape[0] == 2:
        gamematrix = np.transpose(gamematrix)
    elif gamematrix.shape[1] != 2:
        raise Exception(("Shape has to be 2xM or Nx2, but found ", gamematrix.shape))

    X1 = gamematrix[:, 0]
    X2 = gamematrix[:, 1]
    line_origin = [[0, i] for i in X1]
    line_endpoint = [[1, i] for i in X2]
    lines = list(zip(line_origin, line_endpoint))
    _lower_envelope_x_0_1(lines)

    fig, ax = plt.subplots()
    rax = ax.twinx()
    ax.set_xlim(0, 1)
    ax.set_ylim(y_lower_lim, y_upper_lim)
    rax.set_ylim(y_lower_lim, y_upper_lim)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # zero spine
    ax.plot([0, 1], [0, 0], "black")
    make_spines_invisible(rax)
    ax.set_xticks([])
    rax.set_xticks([])
    ax.set_yticks(np.append(X1, 0))
    rax.set_yticks(np.append(X2, 0))

    ax.plot([0, 1], [X1, X2], color)
    plt.show()


graphical_2_solution([[1, 3], [-1, 5], [3, -3], [3, -1], [.5, 2], [1, -2.1], [-.5, 1]])
