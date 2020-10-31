import chemics as cm
import logging
import matplotlib.pyplot as plt


def bc_ult_analysis(ult_bases):
    """
    Biomass composition based on characterization method discussed in Debiagi
    2015 paper. Uses only the C and H mass fractions from ultimate analysis of
    the feedstock.

    Parameters
    ----------
    ult_bases : dict
        Ultimate analysis bases.

    Returns
    -------
    bc_ult : dict
        Biomass composition.
    """

    yc = ult_bases['dafcho'][0] / 100
    yh = ult_bases['dafcho'][1] / 100

    bc = cm.biocomp(yc, yh)

    # log results to console
    results = (
        f'{" Biomass composition ":-^80}\n\n'
        f'Using Debiagi 2015 characterization method.\n'
        f'Using yc, yh as determined from ultimate analysis. Results in mass %.\n'
        f'yc = {yc:.4f}\n'
        f'yh = {yh:.4f}\n\n'
        f'                     % daf\n'
        f'cellulose         {bc["y_daf"][0] * 100:8.2f}\n'
        f'hemicellulose     {bc["y_daf"][1] * 100:8.2f}\n'
        f'lignin-c          {bc["y_daf"][2] * 100:8.2f}\n'
        f'lignin-h          {bc["y_daf"][3] * 100:8.2f}\n'
        f'lignin-o          {bc["y_daf"][4] * 100:8.2f}\n'
        f'tannins           {bc["y_daf"][5] * 100:8.2f}\n'
        f'triglycerides     {bc["y_daf"][6] * 100:8.2f}\n'
    )

    logging.info(results)

    # return daf results for use in reactor model
    bc_ult = {
        'cellulose': bc["y_daf"][0],
        'hemicellulose': bc["y_daf"][1],
        'lignin-c': bc["y_daf"][2],
        'lignin-h': bc["y_daf"][3],
        'lignin-o': bc["y_daf"][4],
        'tannins': bc["y_daf"][5],
        'triglycerides': bc["y_daf"][6]
    }

    # plot biomass characterization
    fig, ax = plt.subplots(tight_layout=True)
    cm.plot_biocomp(ax, yc, yh, bc['y_rm1'], bc['y_rm2'], bc['y_rm3'])

    return bc_ult
