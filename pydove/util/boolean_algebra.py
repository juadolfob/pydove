def comp2(x1, x2, sign):
    if sign == "<": return x1 < x2
    if sign == ">": return x1 > x2
    if sign == "=": return x1 == x2
    if sign == ">=": return x1 >= x2
    if sign == "<=": return x1 <= x2
    # could use "return Rel(x1, x2, 'sign')" but it is slower, an if chain is much faster
    return None