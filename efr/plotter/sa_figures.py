"""
Functions for creating sensitivity analysis figures.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_param_values(pv):
    """
    Plot the parameter values that are used for the batch reactor model.

    Parameters
    ----------
    pv : ndarray
        Parameter values used for input to batch reactor model. Values
        represent the biomass composition as cellulose, hemicellulose,
        lignin-c, lignin-h, lignin-o, tannins, and triglycerides.
    """

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(pv.T, 'o')
    ax.set_xlabel('Biomass composition')
    ax.set_ylabel('Mass fraction [-]')
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xticks(range(7))
    ax.set_xticklabels(['CELL', 'GMSW', 'LIGC', 'LIGH', 'LIGO', 'TANN', 'TGL'])
    ax.tick_params(color='0.9')


def plot_sobol(names, si_gas, si_liquid, si_solid):
    """
    Plot Sobol indices.

    Parameters
    ----------
    names : list
        Labels for the x-axis.
    si_gas : dict
        Sobol indices for gas phase.
    si_liquid : dict
        Sobol indices for liquid phase.
    si_solid : dict
        Sobol indices for solid phase.

    Note
    ----
    Keys available in the si_gas, si_liquid, si_solid dictionaries are S1,
    S1_conf, ST, ST_conf, S2, S2_conf.
    """

    x = np.arange(len(names))
    width = 0.35

    def bar_style(ax):
        ax.grid(True, color='0.9')
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')

    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(13, 4.8), sharey=True, tight_layout=True)

    ax1.bar(x - width / 2, si_gas['S1'], width, label='S1')
    ax1.bar(x + width / 2, si_gas['ST'], width, label='ST')
    ax1.errorbar(x - width / 2, si_gas['S1'], yerr=si_gas['S1_conf'], fmt='k.')
    ax1.errorbar(x + width / 2, si_gas['ST'], yerr=si_gas['ST_conf'], fmt='k.')
    ax1.set_ylabel('Sensitivity')
    ax1.set_title('Gases')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names)
    bar_style(ax1)

    ax2.bar(x - width / 2, si_liquid['S1'], width, label='S1')
    ax2.bar(x + width / 2, si_liquid['ST'], width, label='ST')
    ax2.errorbar(x - width / 2, si_liquid['S1'], yerr=si_liquid['S1_conf'], fmt='k.')
    ax2.errorbar(x + width / 2, si_liquid['ST'], yerr=si_liquid['ST_conf'], fmt='k.')
    ax2.set_title('Liquids')
    ax2.set_xlabel('Parameter')
    ax2.set_xticks(x)
    ax2.set_xticklabels(names)
    bar_style(ax2)

    ax3.bar(x - width / 2, si_solid['S1'], width, label='S1')
    ax3.bar(x + width / 2, si_solid['ST'], width, label='ST')
    ax3.errorbar(x - width / 2, si_solid['S1'], yerr=si_solid['S1_conf'], fmt='k.')
    ax3.errorbar(x + width / 2, si_solid['ST'], yerr=si_solid['ST_conf'], fmt='k.')
    ax3.legend(loc='best')
    ax3.set_title('Solids')
    ax3.set_xticks(x)
    ax3.set_xticklabels(names)
    bar_style(ax3)
