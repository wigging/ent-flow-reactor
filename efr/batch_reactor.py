import cantera as ct
import logging
import numpy as np

from plotter import plot_gases_liquids
from plotter import plot_solids_metaplastics
from plotter import plot_phases_and_temp
from plotter import plot_barh


def batch_reactor(params, bc):
    """
    Batch reactor yields using Debiagi 2018 kinetics for softwood.

    Parameters
    ----------
    params : dict
        Reactor parameters.
    bc : dict
        Biomass composition.
    """

    # get reactor parameters
    tmax = params['time_duration']
    temp = params['temperature']
    press = params['pressure']
    energy = params['energy']

    # get CTI file for Debiagi 2018 kinetics for softwood
    cti_file = params['cti_file']

    # biomass composition as mass fraction inputs to batch reactor
    y_fracs = {
        'CELL': bc['cellulose'],
        'GMSW': bc['hemicellulose'],
        'LIGC': bc['lignin-c'],
        'LIGH': bc['lignin-h'],
        'LIGO': bc['lignin-o'],
        'TANN': bc['tannins'],
        'TGL': bc['triglycerides']
    }

    # time vector to evaluate reaction rates [s]
    time = np.linspace(0, tmax, 100)

    # disable warnings about discontinuity at polynomial mid-point in thermo data
    # comment this line to show the warnings
    ct.suppress_thermo_warnings()

    gas = ct.Solution(cti_file)

    gas.TPY = temp, press, y_fracs
    r = ct.IdealGasReactor(gas, energy=energy)

    sim = ct.ReactorNet([r])
    states = ct.SolutionArray(gas, extra=['t'])

    for tm in time:
        sim.advance(tm)
        states.append(r.thermo.state, t=tm)

    # species representing gases
    sp_gases = ('C2H4', 'C2H6', 'CH2O', 'CH4', 'CO', 'CO2', 'H2')

    # species representing liquids (tars)
    sp_liquids = (
        'C2H3CHO', 'C2H5CHO', 'C2H5OH', 'C5H8O4', 'C6H10O5', 'C6H5OCH3', 'C6H5OH',
        'C6H6O3', 'C24H28O4', 'CH2OHCH2CHO', 'CH2OHCHO', 'CH3CHO', 'CH3CO2H',
        'CH3OH', 'CHOCHO', 'CRESOL', 'FURFURAL', 'H2O', 'HCOOH', 'MLINO', 'U2ME12',
        'VANILLIN', 'ACQUA'
    )

    # species representing solids
    sp_solids = (
        'CELL', 'CELLA', 'GMSW', 'HCE1', 'HCE2', 'ITANN', 'LIG', 'LIGC', 'LIGCC',
        'LIGH', 'LIGO', 'LIGOH', 'TANN', 'TGL', 'CHAR'
    )

    # species representing metaplastics
    sp_metaplastics = (
        'GCH2O', 'GCO2', 'GCO', 'GCH3OH', 'GCH4', 'GC2H4', 'GC6H5OH', 'GCOH2',
        'GH2', 'GC2H6'
    )

    # sum of species mass fractions for gases, liquids, solids, metaplastics
    y_gases = states(*sp_gases).Y.sum(axis=1)
    y_liquids = states(*sp_liquids).Y.sum(axis=1)
    y_solids = states(*sp_solids).Y.sum(axis=1)
    y_metaplastics = states(*sp_metaplastics).Y.sum(axis=1)

    # Logging
    # ------------------------------------------------------------------------

    # log results to console
    results = (
        f'{" Batch reactor ":-^80}\n\n'
        f'pressure      = {press:,} Pa\n'
        f'temperature   = {temp} K ({temp - 273.15}°C)\n'
        f'time duration = {tmax} s\n'
        f'energy        = {energy}\n\n'
        f'              % mass\n'
        f'gases         {y_gases[-1] * 100:.2f}\n'
        f'liquids       {y_liquids[-1] * 100:.2f}\n'
        f'solids        {y_solids[-1] * 100:.2f}\n'
        f'metaplastics  {y_metaplastics[-1] * 100:.2f}\n'
    )

    logging.info(results)

    # Plotting
    # ------------------------------------------------------------------------

    plot_gases_liquids(states, sp_gases, sp_liquids)
    plot_solids_metaplastics(states, sp_metaplastics)
    plot_phases_and_temp(states, y_gases, y_liquids, y_solids, y_metaplastics)
    plot_barh(states, sp_gases, sp_liquids, sp_solids, sp_metaplastics)
