import cantera as ct
import logging
import numpy as np

from plotter import plot_efr_yields


def efr_model(params, biomass):
    """
    Entrained flow reactor (EFR) model. The EFR is modeled as a plug flow
    reactor (PFR) which is represented as a series of continuously stirred
    tank reactors (CSTRs).

    Parameters
    ----------
    params : dict
        Reactor parameters.
    biomass : dict
        Biomass composition.

    Note
    ----
    Measured yields from EFR experiment are:
    total liquid    64.9 wt %
    char            13.9 wt %
    gas             17.2 wt %
    """

    # Disable warnings about discontinuity at polynomial mid-point in thermo data.
    # Remove this line to show the warnings.
    ct.suppress_thermo_warnings()

    # Get parameters
    # ------------------------------------------------------------------------

    diam = params['pipe_inner_diameter']    # m
    length = params['pipe_length']          # m
    temp = params['temperature']            # K

    p_gauge = params['pressure_gauge']      # Pa gauge
    p_atm = params['pressure_atm']          # Pa atmospheric for Golden, CO
    p_abs = p_gauge + p_atm                 # Pa absolute for Golden, CO

    mdot_bio = params['mass_flowrate_biomass']  # kg/hr
    mdot_bio = mdot_bio / 3600                  # convert from kg/hr to kg/s

    mdot_n2 = params['mass_flowrate_n2']        # kg/hr
    mdot_n2 = mdot_n2 / 3600                    # convert from kg/hr to kg/s

    n_cstrs = params['n_cstrs']             # number of CSTRs
    energy = params['energy']               # reactor energy `on` or `off`

    # mass fraction of nitrogen gas from ratio of inlet mass flows
    y_n2 = mdot_n2 / (mdot_n2 + mdot_bio)

    # mass fractions of biomass components where y_bio.sum() = 100.0
    y_bio = np.array(list(biomass.values()))

    # mass fractions of biomass components such that y_bio.sum() + y_n2 = 1.0
    y_bio = (y_bio / y_bio.sum()) * (1 - y_n2)

    # all mass fractions where values sum to 1.0
    y_n2_bio = {
        'N2': y_n2,
        'CELL': y_bio[0],
        'GMSW': y_bio[1],
        'LIGC': y_bio[2],
        'LIGH': y_bio[3],
        'LIGO': y_bio[4],
        'TANN': y_bio[5],
        'TGL': y_bio[6]
    }

    # Setup and run PFR model
    # ------------------------------------------------------------------------

    # Gas phase for the reactor model
    gas = ct.Solution(params['cti_file'])
    gas.TPY = temp, p_abs, y_n2_bio

    # Create a stirred tank reactor (CSTR)
    cstr = ct.IdealGasConstPressureReactor(gas, energy=energy)

    dz = length / n_cstrs
    area = np.pi * (diam**2)
    cstr.volume = area * dz

    # Reservoirs for the inlet and outlet of each CSTR
    inlet = ct.Reservoir(gas)
    outlet = ct.Reservoir(gas)

    # Mass flow rate into the CSTR
    mf = ct.MassFlowController(upstream=inlet, downstream=cstr, mdot=mdot_n2 + mdot_bio)

    # Determine pressure in the CSTR
    ct.PressureController(upstream=cstr, downstream=outlet, master=mf, K=1e-5)

    # Create a reactor network for performing the simulation
    sim = ct.ReactorNet([cstr])

    # Store the results for each CSTR
    states = ct.SolutionArray(cstr.thermo)
    states.append(cstr.thermo.state)

    for n in range(n_cstrs):
        gas.TPY = cstr.thermo.TPY
        inlet.syncState()
        sim.reinitialize()
        sim.advance_to_steady_state()
        states.append(cstr.thermo.state)

    # Group mass fractions into gas, liquid, solid, and metaplastic species
    # ------------------------------------------------------------------------

    sp_gases = ('C2H4', 'C2H6', 'CH2O', 'CH4', 'CO', 'CO2', 'H2', 'N2')

    sp_liquids = (
        'C2H3CHO', 'C2H5CHO', 'C2H5OH', 'C5H8O4', 'C6H10O5', 'C6H5OCH3', 'C6H5OH',
        'C6H6O3', 'C24H28O4', 'CH2OHCH2CHO', 'CH2OHCHO', 'CH3CHO', 'CH3CO2H',
        'CH3OH', 'CHOCHO', 'CRESOL', 'FURFURAL', 'H2O', 'HCOOH', 'MLINO', 'U2ME12',
        'VANILLIN', 'ACQUA')

    sp_solids = (
        'CELL', 'CELLA', 'GMSW', 'HCE1', 'HCE2', 'ITANN', 'LIG', 'LIGC', 'LIGCC',
        'LIGH', 'LIGO', 'LIGOH', 'TANN', 'TGL', 'CHAR')

    sp_metaplastics = (
        'GCH2O', 'GCO2', 'GCO', 'GCH3OH', 'GCH4', 'GC2H4', 'GC6H5OH', 'GCOH2',
        'GH2', 'GC2H6')

    y_n2 = states('N2').Y[:, 0]
    y_gas = states(*sp_gases).Y.sum(axis=1)
    y_liquid = states(*sp_liquids).Y.sum(axis=1)
    y_solid = states(*sp_solids).Y.sum(axis=1)
    y_meta = states(*sp_metaplastics).Y.sum(axis=1)

    # Mass fractions from only biomass (no nitrogen gas)
    sum_bio = y_gas + y_liquid + y_solid + y_meta - y_n2
    y_gas_bio = (y_gas - y_n2) / sum_bio
    y_liquid_bio = y_liquid / sum_bio
    y_solid_bio = y_solid / sum_bio
    y_meta_bio = y_meta / sum_bio

    # Logging
    # ------------------------------------------------------------------------

    results = (
        f'{" Entrained flow reactor ":-^80}\n\n'
        f'mf_biomass    = {params["mass_flowrate_biomass"]}\n'
        f'mf_n2         = {params["mass_flowrate_n2"]}\n'
        f'energy        = {energy}\n'
        f'n_cstrs       = {n_cstrs}\n'

        '\nInlet mass fractions\n'
        f'gas       = {y_gas[0]:.3f}\n'
        f'liquid    = {y_liquid[0]:.3f}\n'
        f'solid     = {y_solid[0]:.3f}\n'
        f'meta      = {y_meta[0]:.3f}\n'
        f'sum       = {y_gas[0] + y_liquid[0] + y_solid[0] + y_meta[0]:.3f}\n'

        '\nFinal mass fractions (N₂ basis)\n'
        f'gas       = {y_gas[-1]:.3f}\n'
        f'liquid    = {y_liquid[-1]:.3f}\n'
        f'solid     = {y_solid[-1]:.3f}\n'
        f'meta      = {y_meta[-1]:.3f}\n'
        f'sum       = {y_gas[-1] + y_liquid[-1] + y_solid[-1] + y_meta[-1]:.3f}\n'

        '\nFinal mass fractions (N₂ free basis)\n'
        f'gas       = {y_gas_bio[-1]:.3f}\n'
        f'liquid    = {y_liquid_bio[-1]:.3f}\n'
        f'solid     = {y_solid_bio[-1]:.3f}\n'
        f'meta      = {y_meta_bio[-1]:.3f}\n'
        f'sum       = {y_gas_bio[-1] + y_liquid_bio[-1] + y_solid_bio[-1] + y_meta_bio[-1]:.3f}\n'

        '\nCompare EFR yields (wt%, N₂ free basis)\n'
        '                exp     model\n'
        f'total liquid    64.9    {y_liquid_bio[-1] * 100:.1f}\n'
        f'char            13.9    {(y_solid_bio[-1] + y_meta_bio[-1]) * 100:.1f}\n'
        f'gas             17.2    {y_gas_bio[-1] * 100:.1f}\n'
        f'sum             96.0    {(y_gas_bio[-1] + y_liquid_bio[-1] + y_solid_bio[-1] + y_meta_bio[-1]) * 100:.1f}\n'
    )

    logging.info(results)

    # Plotting
    # ------------------------------------------------------------------------

    plot_efr_yields(y_gas, y_liquid, y_solid, y_meta, states.T, states.P)
    plot_efr_yields(y_gas_bio, y_liquid_bio, y_solid_bio, y_meta_bio, states.T, states.P)
