"""
Information about the program.
"""

info = {
    'reactor_name': 'Entrained Flow Reactor (EFR)',
    'feedstock_name': 'Blend3',
    'case': 5
}

"""
Parameters for the Blend3 feedstock.

Several biomass compositions for the Blend3 feedstock were investigated in the
report. See below for those cases. Values are reported as % dry.

                Case 3  Case 4  Case 5
cellulose       38.95   38.95   38.95
hemicellulose   23.12   23.12   23.12
lignin-c         9.83    9.83       0
lignin-h         9.83    9.83   14.74
lignin-o         9.83    9.83   14.74
tannins          7.83       0       0
triglycerides       0    7.83    7.83
ash              0.63    0.63    0.63

`ultimate_analysis`
Elements listed as [C, H, O, N, S, ash, moisture].

`chemical_analysis`
Biomass composition determined from chemical analysis data. These values are
used for the pyrolysis kinetics. Composition values are given as mass % on a
dry basis (% dry).

`biomass_characterization`
Selected values for biomass characterization procedure.
"""

feedstock = {
    'name': 'Blend3',

    'ultimate_analysis': [49.52, 5.28, 38.35, 0.15, 0.02, 0.64, 6.04],

    'chemical_analysis': {
        'cellulose': 38.95,
        'hemicellulose': 23.12,
        'lignin_c': 0.0,
        'lignin_h': 14.74,
        'lignin_o': 14.74,
        'tannins': 0.0,
        'triglycerides': 7.83,
        'ash': 0.63
    },

    'biomass_characterization': {
        'yc': 0.51,
        'yh': 0.06,
        'alpha': 0.56,
        'beta': 0.6,
        'gamma': 0.6,
        'delta': 0.78,
        'epsilon': 0.88
    }
}

"""
Parameters for the entrained flow reactor (EFR).

`energy`
Used by the Cantera reactor model. If set to `off` then disable the energy
equation. If `on` then enable the energy and use the provided thermo data for
the reactions.
"""

reactor = {
    'cti_file': 'params/debiagi_sw_n2_mod.cti',
    'energy': 'off',
    'mass_flowrate_biomass': 15.0,
    'mass_flowrate_n2': 15.0,
    'n_cstrs': 20,
    'pipe_inner_diameter': 0.041,
    'pipe_length': 28.7,
    'pressure_gauge': 60_100.0,
    'pressure_atm': 80_900.0,
    'pressure': 101_325.0,
    'temperature': 773.15,
    'time_duration': 10.0
}

"""
Parameters for sensitivity analysis of the Debiagi 2018 kinetics.
"""

sensitivity_analysis = {
    'n_samples': 1000,
    'num_vars': 7,
    'names': ['CELL', 'GMSW', 'LIGC', 'LIGH', 'LIGO', 'TANN', 'TGL'],
    'bounds': [[0.01, 1.00],
               [0.01, 1.00],
               [0.01, 1.00],
               [0.01, 1.00],
               [0.01, 1.00],
               [0.01, 1.00],
               [0.01, 1.00]]
}
