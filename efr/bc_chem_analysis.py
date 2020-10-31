import logging


def bc_chem_analysis(params):
    """
    Biomass composition based on chemical analysis of the feedstock. Uses the
    chemical analysis data of the feedstock to determine the composition.

    Parameters
    ----------
    params : dict
        Feedstock parameters.

    Returns
    -------
    bc_chem : dict
        Biomass composition.
    """

    # dry basis
    cell_dry = params['chemical_analysis']['cellulose']
    hemi_dry = params['chemical_analysis']['hemicellulose']
    ligc_dry = params['chemical_analysis']['lignin_c']
    ligh_dry = params['chemical_analysis']['lignin_h']
    ligo_dry = params['chemical_analysis']['lignin_o']
    tann_dry = params['chemical_analysis']['tannins']
    tgl_dry = params['chemical_analysis']['triglycerides']
    ash = params['chemical_analysis']['ash']
    sum_dry = cell_dry + hemi_dry + ligc_dry + ligh_dry + ligo_dry + tann_dry + tgl_dry + ash

    # dry ash-free basis
    cell_daf = cell_dry / (sum_dry - ash) * 100
    hemi_daf = hemi_dry / (sum_dry - ash) * 100
    ligc_daf = ligc_dry / (sum_dry - ash) * 100
    ligh_daf = ligh_dry / (sum_dry - ash) * 100
    ligo_daf = ligo_dry / (sum_dry - ash) * 100
    tann_daf = tann_dry / (sum_dry - ash) * 100
    tgl_daf = tgl_dry / (sum_dry - ash) * 100
    sum_daf = cell_daf + hemi_daf + ligc_daf + ligh_daf + ligo_daf + tann_daf + tgl_daf

    # log results to console
    results = (
        f'{" Biomass composition ":-^80}\n\n'
        f'Using chemical analysis data. Values reported as mass %.\n\n'
        f'                     % dry    % daf\n'
        f'cellulose         {cell_dry:8.2f} {cell_daf:8.2f}\n'
        f'hemicellulose     {hemi_dry:8.2f} {hemi_daf:8.2f}\n'
        f'lignin-c          {ligc_dry:8.2f} {ligc_daf:8.2f}\n'
        f'lignin-h          {ligh_dry:8.2f} {ligh_daf:8.2f}\n'
        f'lignin-o          {ligo_dry:8.2f} {ligo_daf:8.2f}\n'
        f'tannins           {tann_dry:8.2f} {tann_daf:8.2f}\n'
        f'triglycerides     {tgl_dry:8.2f} {tgl_daf:8.2f}\n'
        f'sum               {sum_dry:8.2f} {sum_daf:8.2f}\n'
    )

    logging.info(results)

    # return daf results for use in reactor model
    bc_chem = {
        'cellulose': cell_daf,
        'hemicellulose': hemi_daf,
        'lignin-c': ligc_daf,
        'lignin-h': ligh_daf,
        'lignin-o': ligo_daf,
        'tannins': tann_daf,
        'triglycerides': tgl_daf
    }

    return bc_chem
