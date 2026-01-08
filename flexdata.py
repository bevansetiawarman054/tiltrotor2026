import pandas as pd

flex = pd.read_csv('Mode8.csv')


def y():
    return flex.y


def R2():
    return flex.R2*0.1


def T3():
    return flex.T3*0.1
