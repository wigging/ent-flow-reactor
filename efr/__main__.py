import argparse
import importlib
import logging
import matplotlib.pyplot as plt
import timeit

from general_info import general_info
from ult_analysis_bases import ult_analysis_bases
from bc_chem_analysis import bc_chem_analysis
from bc_ult_analysis import bc_ult_analysis
from bc_ult_modified import bc_ult_modified
from batch_reactor import batch_reactor
from batch_sensitivity import batch_sensitivity
from efr_model import efr_model


def _command_line_args():
    """
    Command line arguments.
    """

    parser = argparse.ArgumentParser(
        description='🚀 Entrained flow reactor (EFR) program',
        epilog='🤓 Enjoy the program.')

    parser.add_argument(
        'path_params',
        help='path to parameters module file')

    parser.add_argument(
        '-bc', '--biocomp',
        choices=['chem', 'ult', 'ultmod'],
        default='chem',
        help='biomass composition method (default: chem)')

    parser.add_argument(
        '-ba', '--batch',
        action='store_true',
        help='run a batch reactor model')

    parser.add_argument(
        '-sa', '--sensanalysis',
        action='store_true',
        help='run a batch reactor sensitivity analysis')

    parser.add_argument(
        '-em', '--efrmodel',
        action='store_true',
        help='run entrained flow reactor model')

    parser.add_argument(
        '-sp', '--showplots',
        action='store_true',
        help='show plot figures')

    args = parser.parse_args()
    return args


def main():
    """
    Main function to run the program.
    """

    # Start time for the program
    ti = timeit.default_timer()

    # Configure logging and get command line arguments
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    args = _command_line_args()

    # Get file path and module name of the parameters file
    # Import the parameters as a `params` Python module
    file_path = args.path_params
    module_name = args.path_params.split('/')[1]

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)

    # General information
    general_info(params)

    # Ultimate analysis bases
    ult_bases = ult_analysis_bases(params.feedstock)

    # Biomass composition
    if args.biocomp == 'chem':
        bc = bc_chem_analysis(params.feedstock)
    elif args.biocomp == 'ult':
        bc = bc_ult_analysis(ult_bases)
    elif args.biocomp == 'ultmod':
        bc = bc_ult_modified(params.feedstock)

    # Batch reactor yields using biomass composition
    if args.batch:
        batch_reactor(params.reactor, bc)

    # Batch reactor sensitivity analysis using Debiagi 2018 pyrolysis kinetics
    if args.sensanalysis:
        batch_sensitivity(params.reactor, params.sensitivity_analysis)

    # Entrained flow reactor model using biomass composition
    if args.efrmodel:
        efr_model(params.reactor, bc)

    # Elapsed time for the program
    tf = timeit.default_timer()
    dt = tf - ti
    minutes, seconds = divmod(dt, 60)
    logging.info(
        f'\n{" Done ":-^80}\n\n'
        f'elapsed time = {dt:.2f} seconds (≈ {minutes} min {seconds:.0f} sec)'
    )

    # Show all plot figures
    if args.showplots:
        plt.show()


if __name__ == '__main__':
    main()
