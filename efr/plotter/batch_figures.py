"""
Functions for creating batch reactor figures.
"""

import matplotlib.pyplot as plt
import numpy as np


def _style_line(ax, xlabel, ylabel, title=None, legend=None):
    """
    Configure and style the plot figure.
    """
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')

    if title:
        ax.set_title(title)

    if legend == 'side':
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    elif legend == 'best':
        ax.legend(loc='best', frameon=False)


def _style_barh(ax):
    """
    Style for barh plot.
    """
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.tick_params(color='0.8')
    ax.xaxis.grid(True, color='0.8')


def plot_gases_liquids(states, sp_gases, sp_liquids):
    """
    Plot batch reactor gases and liquids concentrations.
    """
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 4.8), sharey=True, tight_layout=True)

    # gases
    for sp in sp_gases:
        ax1.plot(states.t, states(sp).Y[:, 0], label=sp.translate(SUB))

    _style_line(ax1, xlabel='Time [s]', ylabel='Mass fraction [-]', title='Gases', legend='side')

    # liquids
    for sp in sp_liquids[:len(sp_liquids) // 2]:
        ax2.plot(states.t, states(sp).Y[:, 0], label=sp.translate(SUB))

    for sp in sp_liquids[len(sp_liquids) // 2:]:
        ax3.plot(states.t, states(sp).Y[:, 0], label=sp.translate(SUB))

    _style_line(ax2, xlabel='Time [s]', ylabel='', title='Liquids', legend='side')
    _style_line(ax3, xlabel='Time [s]', ylabel='', title='Liquids', legend='side')


def plot_solids_metaplastics(states, sp_metaplastics):
    """
    Plot batch reactor solids and metaplastics concentrations.
    """
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 6), tight_layout=True)

    # solids (biomass composition)
    axs[0, 0].plot(states.t, states('CELL').Y[:, 0], label='CELL')
    axs[0, 0].plot(states.t, states('GMSW').Y[:, 0], label='GMSW')
    axs[0, 0].plot(states.t, states('LIGC').Y[:, 0], label='LIGC')
    axs[0, 0].plot(states.t, states('LIGH').Y[:, 0], label='LIGH')
    axs[0, 0].plot(states.t, states('LIGO').Y[:, 0], label='LIGO')
    axs[0, 0].plot(states.t, states('TANN').Y[:, 0], label='TANN')
    axs[0, 0].plot(states.t, states('TGL').Y[:, 0], label='TGL')
    axs[0, 0].get_shared_y_axes().join(axs[0, 0], axs[0, 1])
    _style_line(axs[0, 0], xlabel='Time [s]', ylabel='Mass fraction [-]', title='Solids', legend='side')

    # solids
    axs[0, 1].plot(states.t, states('CELLA').Y[:, 0], label='CELLA')
    axs[0, 1].plot(states.t, states('HCE1').Y[:, 0], label='HCE1')
    axs[0, 1].plot(states.t, states('HCE2').Y[:, 0], label='HCE2')
    axs[0, 1].plot(states.t, states('ITANN').Y[:, 0], label='ITANN')
    axs[0, 1].plot(states.t, states('LIG').Y[:, 0], label='LIG')
    axs[0, 1].plot(states.t, states('LIGCC').Y[:, 0], label='LIGCC')
    axs[0, 1].plot(states.t, states('LIGOH').Y[:, 0], label='LIGOH')
    axs[0, 1].plot(states.t, states('CHAR').Y[:, 0], label='CHAR')
    _style_line(axs[0, 1], xlabel='Time [s]', ylabel='', title='Solids', legend='side')

    # metaplastics
    for sp in sp_metaplastics[:len(sp_metaplastics) // 2]:
        axs[1, 0].plot(states.t, states(sp).Y[:, 0], label=sp.translate(SUB))

    axs[1, 0].get_shared_y_axes().join(axs[1, 0], axs[1, 1])
    _style_line(axs[1, 0], xlabel='Time [s]', ylabel='Mass fraction [-]', title='Metaplastics', legend='side')

    # metaplastics
    for sp in sp_metaplastics[len(sp_metaplastics) // 2:]:
        axs[1, 1].plot(states.t, states(sp).Y[:, 0], label=sp.translate(SUB))

    _style_line(axs[1, 1], xlabel='Time [s]', ylabel='', title='Metaplastics', legend='side')


def plot_phases_and_temp(states, y_gases, y_liquids, y_solids, y_metaplastics):
    """
    Plot batch reactor concentrations as phases such as gases, liquids,
    solids, and metaplastics. Plot batch reactor temperature.
    """
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4.8), tight_layout=True)

    # phases
    ax1.plot(states.t, y_gases, label='gases')
    ax1.plot(states.t, y_liquids, label='liquids')
    ax1.plot(states.t, y_solids, label='solids')
    ax1.plot(states.t, y_metaplastics, label='metaplastics')
    _style_line(ax1, xlabel='Time [s]', ylabel='Mass fraction [-]', legend='best')

    # temperature
    ax2.plot(states.t, states.T, color='m')
    _style_line(ax2, xlabel='Time [s]', ylabel='Temperature [K]')


def plot_barh(states, sp_gases, sp_liquids, sp_solids, sp_metaplastics):
    """
    Plot final batch reactor concentrations as horizontal bars for gases,
    liquids, solids, and metaplastics.
    """
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(12, 6), tight_layout=True)

    # gases
    yg = [states(sp).Y[:, 0][-1] for sp in sp_gases]
    yg_pos = np.arange(len(sp_gases))

    ax1.barh(yg_pos, yg, align='center', color='C0', height=0.4)
    ax1.set_title('Gases')
    ax1.set_xlabel('Mass fraction [-]')
    ax1.set_ylim(min(yg_pos) - 1, max(yg_pos) + 1)
    ax1.set_yticks(yg_pos)
    ax1.set_yticklabels(sp_gases)
    _style_barh(ax1)

    # liquids
    yl = [states(sp).Y[:, 0][-1] for sp in sp_liquids]
    yl_pos = np.arange(len(sp_liquids))

    ax2.barh(yl_pos, yl, align='center', color='C1')
    ax2.set_title('Liquids')
    ax2.set_xlabel('Mass fraction [-]')
    ax2.set_ylim(min(yl_pos) - 1, max(yl_pos) + 1)
    ax2.set_yticks(yl_pos)
    ax2.set_yticklabels(sp_liquids)
    _style_barh(ax2)

    # solids
    ys = [states(sp).Y[:, 0][-1] for sp in sp_solids]
    ys_pos = np.arange(len(sp_solids))

    ax3.barh(ys_pos, ys, align='center', color='C2')
    ax3.set_title('Solids')
    ax3.set_xlabel('Mass fraction [-]')
    ax3.set_ylim(min(ys_pos) - 1, max(ys_pos) + 1)
    ax3.set_yticks(ys_pos)
    ax3.set_yticklabels(sp_solids)
    _style_barh(ax3)

    # metaplastics
    ym = [states(sp).Y[:, 0][-1] for sp in sp_metaplastics]
    ym_pos = np.arange(len(sp_metaplastics))

    ax4.barh(ym_pos, ym, align='center', color='C3', height=0.55)
    ax4.set_title('Metaplastics')
    ax4.set_xlabel('Mass fraction [-]')
    ax4.set_ylim(min(ym_pos) - 1, max(ym_pos) + 1)
    ax4.set_yticks(ym_pos)
    ax4.set_yticklabels(sp_metaplastics)
    _style_barh(ax4)


def plot_batch_effects(param_values, y_out):
    """
    Plot effects of cellulose, hemicellulose, lignin-c, lignin-h,  lignin-o,
    tann, and tgl on batch reactor yields for sensitivity analysis. Yields are
    presented as grouped chemical species of gases, liquids, and solids.

    Parameters
    ----------
    params_values : ndarray
        Samples generated using Saltelli’s sampling scheme. These samples are
        inputs to the batch reactor model.
    y_out : ndarray
        Batch reactor outputs from the generated Saltelli samples.
    """

    # --- Figure 1 ---
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(13.5, 8), tight_layout=True)

    # cellulose for rows 0, 1, 2 and column 0
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 0].hexbin(param_values[:, 0], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 0].axis([param_values[:, 0].min(), param_values[:, 0].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 0].set_xlabel('CELL')
        axs[i, 0].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 0])     # colorbar represents counts

    # hemicellulose for rows 0, 1, 2 and column 1
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 1].hexbin(param_values[:, 1], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 1].axis([param_values[:, 1].min(), param_values[:, 1].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 1].set_xlabel('GMSW')
        axs[i, 1].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 1])

    # lignin-c for rows 0, 1, 2 and column 2
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 2].hexbin(param_values[:, 2], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 2].axis([param_values[:, 2].min(), param_values[:, 2].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 2].set_xlabel('LIGC')
        axs[i, 2].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 2])

    # lignin-h for rows 0, 1, 2 and column 3
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 3].hexbin(param_values[:, 3], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 3].axis([param_values[:, 3].min(), param_values[:, 3].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 3].set_xlabel('LIGH')
        axs[i, 3].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 3])

    # --- Figure 2 ---
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(10, 8), tight_layout=True)

    # lignin-o for rows 0, 1, 2 and column 0
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 0].hexbin(param_values[:, 4], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 0].axis([param_values[:, 4].min(), param_values[:, 4].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 0].set_xlabel('LIGO')
        axs[i, 0].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 0])     # colorbar represents counts

    # tann for rows 0, 1, 2 and column 1
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 1].hexbin(param_values[:, 5], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 1].axis([param_values[:, 5].min(), param_values[:, 5].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 1].set_xlabel('TANN')
        axs[i, 1].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 1])

    # tgl for rows 0, 1, 2 and column 2
    for i, g in enumerate(['Gases', 'Liquids', 'Solids']):
        hb = axs[i, 2].hexbin(param_values[:, 6], y_out[:, i], gridsize=50, cmap='viridis')
        axs[i, 2].axis([param_values[:, 6].min(), param_values[:, 6].max(), y_out[:, i].min(), y_out[:, i].max()])
        axs[i, 2].set_xlabel('TGL')
        axs[i, 2].set_ylabel(g)
        fig.colorbar(hb, ax=axs[i, 2])
