import math
import aerodata as coeffs
import flexdata as flex
import numpy as np


def sign(x):
    return math.copysign(1, x)


def R(theta):  # compute rotation matrix
    R = np.array([
        [math.cos(theta), math.sin(theta)],
        [-math.sin(theta), math.cos(theta)]
    ])
    return R


def divide2(w, u):
    # w/u
    if abs(u) < 1e-6:
        if u != 0:
            return w/(1e-6)*sign(u)
        else:
            return w/(1e-6)
    else:
        return w/u


def computeqc2v(q, c, V):
    if abs(2*V) < 1e-6:
        return q*c/(1e-6)*(V**2/(V**2+1))

    else:
        return 0.5*q*c/V*(V**2/(V**2+1))

# states: u, w, q, theta, xe, ze, deta, eta, tau


def computeforces(x, params, inp):
    # Inputs
    de = inp[3]
    T_aft = max(0, inp[2])
    T_fwd = max(0, inp[0])
    # System Params
    S = params['S']
    c = params['c']
    rho = params['rho']
    R_aft = params['R_aft']
    R_fwd = params['R_fwd']

    # Pre allocate empty force vector
    forces = np.zeros(4)
    u, w, q, theta, xe, ze, deta, eta, tau = x
    # Precompute Flight Params
    V = math.sqrt(u**2 + w**2)
    q_dyn = 0.5*rho*V**2
    alpha = math.atan2(w, u)
    qc2v = computeqc2v(q, c, V)
    static_coeffs = coeffs.static_coeffs()
    # Compute total coefficients
    cltot = static_coeffs['cl0'] + coeffs.lookup_cl_alpha(alpha) + coeffs.lookup_cl_de(
        de) + static_coeffs['clq']*qc2v + static_coeffs['cl_eta']*eta + coeffs.lookup_cldeta(V)*deta
    cdtot = static_coeffs['cd0'] + coeffs.lookup_cd_alpha(
        alpha) + coeffs.lookup_cd_de(de) + static_coeffs['cdq']*qc2v
    cmtot = static_coeffs['cm0'] + coeffs.lookup_cm_alpha(
        alpha) + coeffs.lookup_cm_de(de) + static_coeffs['cmq']*qc2v + static_coeffs['cm_eta']*eta + coeffs.lookup_cmdeta(V)*deta
    cFxtotal = static_coeffs['cFx0'] + static_coeffs['cFxa']*alpha + coeffs.lookup_cfxq(
        V)*q + static_coeffs['cFx_eta']*eta + coeffs.lookup_cfxdeta(V)*deta
    cCtotal = static_coeffs['cC0'] + static_coeffs['cCa']*alpha + coeffs.lookup_ccq(
        V)*q + static_coeffs['cC_eta']*eta + coeffs.lookup_ccdeta(V)*deta

    # Compute Lift Drag and Moment
    Lift = q_dyn*S*cltot
    Drag = q_dyn*S*cdtot
    Maero = q_dyn*S*cmtot*c

    # Compute Body Forces
    Xaero = Lift*math.sin(alpha) - Drag*math.cos(alpha)
    Zaero = -Lift*math.cos(alpha) - Drag*math.sin(alpha)

    Zpropaft = -T_aft
    Mpropaft = -T_aft*R_aft

    tau_0 = tau + flex.R2()[0]*eta

    Xpropfwd = T_fwd*math.cos(tau_0)
    Zpropfwd = -T_fwd*math.sin(tau_0)
    Mpropfwd = T_fwd*(math.sin(tau_0)*R_fwd + eta *
                      flex.T3()[0]*math.cos(tau_0))

    Qetaprop = T_fwd*math.sin(tau)*(R_fwd*flex.R2()[0]-flex.T3()[0])
    Qetaaero = q_dyn*S*c*(cFxtotal*math.cos(alpha)+cCtotal)

    forces[0] = Xaero + Xpropfwd
    forces[1] = Zaero + Zpropaft + Zpropfwd
    forces[2] = Maero + Mpropaft + Mpropfwd
    forces[3] = Qetaaero + Qetaprop

    return forces
