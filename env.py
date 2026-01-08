from scipy.integrate import solve_ivp
import numpy as np
# import matplotlib.pyplot as plt
import math
import raybe_plot as rplt
import operating_points as op
import computeforces as F
# aerodynamic coefficients

params = {'c': 0.263,  # MAC
          'S': 0.441,  # Reference Area
          'g': 9.81,  # gravity
          'm': 4.5,  # Raybe Mass
          'Iyy': 0.13,  # Raybe Inertia
          'w1': 6.0,  # Flexible Mode 1 Nat.Freq in rad/s
          'rho': 1.225,  # Density
          'R_aft': 0.5,  # meters, moment arm motor aft
          'R_fwd': 0.15,  # meters, moment arm motor fwd
          }


def raybe_eom(t, x, params, inp):
    # inp = t_fwd, tiltrate, t_aft, dE
    g = params['g']
    m = params['m']
    Iyy = params['Iyy']
    w1 = params['w1']

    # System Parameters
    u, w, q, theta, xe, ze, deta, eta, tau = x

    forces = F.computeforces(x, params, inp)
    X = forces[0]
    Z = forces[1]
    M = forces[2]
    Q1 = forces[3]

    # force_history.append((t, X, Z, M, Q1))

    c = math.cos(theta)
    s = math.sin(theta)
    ue = c*u + s*w
    we = -s*u + c*w

    # uw = np.array([u, w])
    # ue, we = np.matmul(F.R(theta), uw)

    dx = np.empty_like(x)

    # Rigid Body Mode
    dx[0] = -g*math.sin(theta) - q*w + X/m  # u dot
    dx[1] = g*math.cos(theta) + q*u + Z/m  # w dot
    dx[2] = M/Iyy  # q dot
    dx[3] = q  # theta dot = q
    dx[4] = ue  # xe dot
    dx[5] = we  # ze dot

    # Flexible Mode
    dx[6] = Q1 - w1**2*eta  # eta ddot
    dx[7] = deta  # eta dot

    # Tilting Rotor
    dx[8] = inp[1]
    return dx


# simulate
# states: u, w, q, theta, xe, ze, deta, eta, tau
x0, inp0 = op.steadycruise25()

sol = solve_ivp(raybe_eom, (0, 10), x0, method='Radau',
                args=(params, inp0,), rtol=1e-8, atol=1e-8)
