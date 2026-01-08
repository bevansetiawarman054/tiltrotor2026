import math
# states: u, w, q, theta, xe, ze, deta, eta, tau


def steadyhover0():
    x0 = (0.01, 0.01, 0, 0.00065052, 0, 0, 0, 0.29818, math.pi/2)
    inp0 = (33.9618, 0, 10.1831, 4.219e-05)
    return x0, inp0


def steadycruise25():
    x0 = (25, 0.37652, 0, 0.01506, 0, 0, 0, 0.067849, 0)
    inp0 = (5.5215, 0, 0.68849, -0.058089)
    return x0, inp0
