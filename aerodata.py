import pandas as pd
import numpy as np

wb = pd.read_excel('lookups.xlsx', sheet_name='wb')
de = pd.read_excel('lookups.xlsx', sheet_name='dE')
elastic = pd.read_excel('lookups.xlsx', sheet_name='elastic')
cons = pd.read_excel('lookups.xlsx', sheet_name='cons')


def static_coeffs():
    return {
        'cl0': cons.cl0.item(),
        'clq': cons.clq.item(),
        'cd0': cons.cd0.item(),
        'cdq': cons.cdq.item(),
        'cm0': cons.cm0.item(),
        'cmq': cons.cmq.item(),
        'cFx0': elastic.cFx0.iloc[0],
        'cFxa': elastic.cFxa.iloc[0],
        'cFx_eta': elastic.cFx_eta.iloc[0],
        'cC0': elastic.cC0.iloc[0],
        'cCa': elastic.cCa.iloc[0],
        'cC_eta': elastic.cC_eta.iloc[0],
        'cl_eta': elastic.cl_eta.iloc[0],
        'cm_eta': elastic.cm_eta.iloc[0],
    }


def lookup_cl_alpha(alpha):
    return np.interp(alpha, wb['alpha_breakpoint'], wb['cla'])


def lookup_cd_alpha(alpha):
    return np.interp(alpha, wb['alpha_breakpoint'], wb['cda'])


def lookup_cm_alpha(alpha):
    return np.interp(alpha, wb['alpha_breakpoint'], wb['cma'])


def lookup_cl_de(edef):
    return np.interp(edef, de['de_breakpoint'], de['clde'])


def lookup_cd_de(edef):
    return np.interp(edef, de['de_breakpoint'], de['cdde'])


def lookup_cm_de(edef):
    return np.interp(edef, de['de_breakpoint'], de['cmde'])


def lookup_cfxq(V):
    return np.interp(V, elastic.u_list, elastic.cFxq)


def lookup_cfxdeta(V):
    return np.interp(V, elastic.u_list, elastic.cFx_eta_dot)


def lookup_ccq(V):
    return np.interp(V, elastic.u_list, elastic.cCq)


def lookup_ccdeta(V):
    return np.interp(V, elastic.u_list, elastic.cC_eta_dot)


def lookup_cldeta(V):
    return np.interp(V, elastic.u_list, elastic.cl_eta_dot)


def lookup_cmdeta(V):
    return np.interp(V, elastic.u_list, elastic.cm_eta_dot)
