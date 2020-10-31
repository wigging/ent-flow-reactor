"""
Function for creating entrained flow reactor figures.
"""

import matplotlib.pyplot as plt


def _config(ax, xlabel, ylabel, title=None, legend=None):
    """
    Configure and style the plot figure.
    """
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')

    if legend == 'side':
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    elif legend == 'best':
        ax.legend(loc='best', frameon=False)


def plot_efr_yields(y_gas, y_liquid, y_solid, y_meta, temp, press):
    """
    Plot entrained flow reactor yields.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(10, 4.8), tight_layout=True)

    ax1.plot(y_gas, label='gas')
    ax1.plot(y_liquid, label='liquid')
    ax1.plot(y_solid, label='solid')
    ax1.plot(y_meta, label='meta')
    _config(ax1, xlabel='CSTR [-]', ylabel='Mass fraction [-]', legend='best')

    ax2.plot(temp)
    _config(ax2, xlabel='CSTR [-]', ylabel='Temperature [K]')

    ax3.plot(press / 1000)
    _config(ax3, xlabel='CSTR [-]', ylabel='Pressure [kPa]')
