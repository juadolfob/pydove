from __future__ import division

import matplotlib.pyplot as plt
import numpy as np


def make_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def slope(origin, endpoint):
    return (endpoint[1] - origin[1]) / (endpoint[0] - origin[0])


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def intersection(L1, L2, point_intersect=True):
    L1 = line(*L1)
    L2 = line(*L2)
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
    # todo fix A and B for lines with sharing points ( slope )

    minimum = min(lines_slope, key=lambda el: el[0][1])
    indices = [i for i, v in enumerate(lines_slope) if v[0][1] == minimum[0][1]]
    A = [lines_slope[min(indices, key=lambda el: lines_slope[el][2])]]

    minimum = min(lines_slope, key=lambda el: el[1][1])
    indices = [i for i, v in enumerate(lines_slope) if v[1][1] == minimum[1][1]]
    B = lines_slope[max(indices, key=lambda el: lines_slope[el][2])]
    print(A, B)
    A_intersections = []
    # line[2] is the slope
    # if A[-1][2] < line[2]:
    while not A[-1] == B:
        next_lines = [l_s for l_s in lines_slope if l_s[2] < A[-1][2]]
        # print("Nezt ", next_lines)
        # print("A ", A)
        next_lines_intersections = []
        for l_s in next_lines:
            line_intersect = intersection(l_s[:2], A[-1][:2], point_intersect=False)
            next_lines_intersections.append(line_intersect)

        # print("Nezt_i ", next_lines_intersections)

        min_intersection = min(enumerate(next_lines_intersections), key=lambda x: x[1][0])
        A_intersections.append(min_intersection)
        A.append(lines_slope[min_intersection[0]])
        del lines_slope[min_intersection[0]]
    return [el[0:2] for el in A], [el[1] for el in A_intersections]


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
    le_lines, le_intersec = _lower_envelope_x_0_1(lines)
    # print(le_lines, le_intersec)
    v_u = max(le_intersec, key=lambda el: el[0])
    print(v_u)
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
    ax.plot([0, 1], [X1, X2], color, linewidth=1)
    # lower envelope
    for le_l in le_lines:
        print(le_l)
        ax.plot([0, 1], [le_l[0][1], le_l[1][1]], "red", linewidth=1.1)
    ax.plot(v_u[0], v_u[1], 'd', color="salmon", linewidth=2, markersize=12)
    plt.show()


graphical_2_solution(
    [[-4, -2.8], [-7, 0], [-4, 0], [0, -4], [-2, -2], [2.9, -3], [2.9, -1.5], [-1.5, -1.5], [-1.5, -1.5], [-2, 5],
     [1, 3], [-1, 5], [3, -3], [3, -1], [.5, 2], [1, -2.1], [-.5, 1], [-.7, 1.9]])
