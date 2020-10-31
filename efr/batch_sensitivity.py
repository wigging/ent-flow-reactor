import cantera as ct
import logging
import numpy as np

from SALib.sample import saltelli
from SALib.analyze import sobol

from plotter import plot_param_values
from plotter import plot_batch_effects
from plotter import plot_sobol


def _run_batch_reactor(y, params):
    """
    Run batch reactor for sensitivity analysis.

    Parameters
    ----------
    y : dict
        Initial biomass composition for CELL, GMSW, LIGC, LIGH, LIGO, TANN,
        and TGL.
    params : dict
        Reactor parameters.

    Returns
    -------
    tuple
        Final mass fraction of y_gases, y_liquids, and y_solids for a given
        time duration.
    """

    # disable warnings about polynomial mid-point discontinuity in thermo data
    ct.suppress_thermo_warnings()

    # get reactor parameters
    tmax = params['time_duration']

    # get reactor parameters
    tmax = params['time_duration']
    temp = params['temperature']
    press = params['pressure']
    energy = params['energy']

    # get CTI file for Debiagi 2018 kinetics for softwood
    cti_file = 'efr/debiagi_sw.cti'

    # time vector to evaluate reaction rates [s]
    time = np.linspace(0, tmax, 100)

    # gas phase
    gas = ct.Solution(cti_file)
    gas.TPY = temp, press, y

    # reactor and states
    r = ct.IdealGasReactor(gas, energy=energy)
    sim = ct.ReactorNet([r])
    states = ct.SolutionArray(gas, extra=['t'])

    for tm in time:
        sim.advance(tm)
        states.append(r.thermo.state, t=tm)

    # species representing gases
    sp_gases = ('C2H4', 'C2H6', 'CH2O', 'CH4', 'CO', 'CO2', 'H2')

    # species representing liquids
    sp_liquids = (
        'C2H3CHO', 'C2H5CHO', 'C2H5OH', 'C5H8O4', 'C6H10O5', 'C6H5OCH3', 'C6H5OH',
        'C6H6O3', 'C24H28O4', 'CH2OHCH2CHO', 'CH2OHCHO', 'CH3CHO', 'CH3CO2H',
        'CH3OH', 'CHOCHO', 'CRESOL', 'FURFURAL', 'H2O', 'HCOOH', 'MLINO', 'U2ME12',
        'VANILLIN', 'ACQUA'
    )

    # species representing solids
    sp_solids = (
        'CELL', 'CELLA', 'GMSW', 'HCE1', 'HCE2', 'ITANN', 'LIG', 'LIGC', 'LIGCC',
        'LIGH', 'LIGO', 'LIGOH', 'TANN', 'TGL', 'CHAR', 'GCH2O', 'GCO2', 'GCO',
        'GCH3OH', 'GCH4', 'GC2H4', 'GC6H5OH', 'GCOH2', 'GH2', 'GC2H6'
    )

    # sum of gases, liquids, and solids mass fractions
    y_gases = states(*sp_gases).Y.sum(axis=1)
    y_liquids = states(*sp_liquids).Y.sum(axis=1)
    y_solids = states(*sp_solids).Y.sum(axis=1)

    # return final mass fractions
    return y_gases[-1], y_liquids[-1], y_solids[-1]


def batch_sensitivity(params, sens_analysis):
    """
    Perform a sensitivity analysis of the Debiagi 2018 pyrolysis kinetics
    using the Sobol method. The Saltelli method is used to generate samples
    for the analysis. Each sample represents a biomass composition in terms of
    [CELL, GMSW, LIGC, LIGH, LIGO, TANN, TGL].

    Parameters
    ----------
    params : dict
        Reactor parameters.
    sens_analysis : dict
        Sensitivity analysis parameters.

    Notes
    -----
    S1 is the first-order sensitivity indices. S1_conf is the first-order
    confidence (can be interpreted as error). ST is the total-order indices
    while ST_conf is total-order confidence.

    Samples generated for the analysis are scaled such that sum is one. This
    ensures that the mass fraction does not exceed one.
    """

    # number of samples to generate for sensitivity analysis
    n = sens_analysis['n_samples']

    # define problem for sensitivity analysis
    problem = {
        'num_vars': sens_analysis['num_vars'],
        'names': sens_analysis['names'],
        'bounds': sens_analysis['bounds']
    }

    # generate samples using Saltelli’s sampling scheme
    param_vals = saltelli.sample(problem, n, calc_second_order=False)

    # scale all samples so they sum to 1
    param_values = param_vals / param_vals.sum(axis=1, keepdims=True)

    # store outputs from batch reactor
    # each row of y_out is [y_gases, y_liquids, y_solids]
    y_out = np.zeros([param_values.shape[0], 3])

    for i, p in enumerate(param_values):
        keys = problem['names']
        y = dict(zip(keys, p))
        y_out[i] = _run_batch_reactor(y, params)

    # perform Sobol analysis for gas, liquid, and solid phases
    si_gas = sobol.analyze(problem, y_out[:, 0], calc_second_order=False)
    si_liquid = sobol.analyze(problem, y_out[:, 1], calc_second_order=False)
    si_solid = sobol.analyze(problem, y_out[:, 2], calc_second_order=False)

    # Logging
    # ------------------------------------------------------------------------

    # log sensitivity analysis parameters to console
    results1 = (
        f'{" Sensitivity analysis ":-^80}\n\n'
        f'Using Sobol analysis for batch reactor with Debiagi 2018 kinetics.\n'
        f'n         = {n:,}\n'
        f'shape     = {param_values.shape}\n'
        f'samples   = {param_values.shape[0]:,}\n'
    )
    logging.info(results1)

    # log results for gases to console
    results2 = (
        f'Sobol analysis for gases:\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results2)

    for i, name in enumerate(problem['names']):
        s1 = si_gas['S1'][i]
        s1conf = si_gas['S1_conf'][i]
        st = si_gas['ST'][i]
        stconf = si_gas['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    # log results for liquids to console
    results3 = (
        f'\nSobol analysis for liquids:\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results3)

    for i, name in enumerate(problem['names']):
        s1 = si_liquid['S1'][i]
        s1conf = si_liquid['S1_conf'][i]
        st = si_liquid['ST'][i]
        stconf = si_liquid['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    # log results for solids to console
    results4 = (
        f'\nSobol analysis for solids:\n\n'
        f'{"Parameter":10} {"S1":>10} {"S1_conf":>10} {"ST":>10} {"ST_conf":>10}'
    )
    logging.info(results4)

    for i, name in enumerate(problem['names']):
        s1 = si_solid['S1'][i]
        s1conf = si_solid['S1_conf'][i]
        st = si_solid['ST'][i]
        stconf = si_solid['ST_conf'][i]
        logging.info(f'{name:10} {s1:10.4f} {s1conf:10.4f} {st:10.4f} {stconf:10.4f}')

    # Plotting
    # ------------------------------------------------------------------------

    plot_param_values(param_values)
    plot_batch_effects(param_values, y_out)
    plot_sobol(problem['names'], si_gas, si_liquid, si_solid)
