# raybe_plot.py
import matplotlib.pyplot as plt
import numpy as np


def plot_solution(sol, force_history=None):
    t = sol.t
    y = sol.y
    state_labels = ['u', 'w', 'q', 'theta', 'xe', 'ze', 'deta', 'eta', 'tau']

    # --- state plots ---
    fig, axes = plt.subplots(3, 3, figsize=(10, 8), sharex=True)
    axes = axes.ravel()

    for i in range(y.shape[0]):
        axes[i].plot(t, y[i, :])
        axes[i].set_ylabel(state_labels[i])

    for ax in axes[-3:]:
        ax.set_xlabel('t [s]')

    plt.tight_layout()

    # --- force history plots (if provided) ---
    if force_history is not None and len(force_history) > 0:
        fh = np.array(force_history)        # shape (N_eval, 5)
        tf = fh[:, 0]
        X = fh[:, 1]
        Z = fh[:, 2]
        M = fh[:, 3]
        Q1 = fh[:, 4]

        fig2, ax2 = plt.subplots(2, 2, figsize=(10, 6), sharex=True)
        ax2 = ax2.ravel()

        ax2[0].plot(tf, X)
        ax2[0].set_ylabel('X [N]')
        ax2[1].plot(tf, Z)
        ax2[1].set_ylabel('Z [N]')
        ax2[2].plot(tf, M)
        ax2[2].set_ylabel('M [Nm]')
        ax2[3].plot(tf, Q1)
        ax2[3].set_ylabel('Q_eta')

        for ax in ax2[2:]:
            ax.set_xlabel('t [s]')

        plt.tight_layout()

    plt.show()
