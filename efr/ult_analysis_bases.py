import logging


def ult_analysis_bases(params):
    """
    Calculate dry basis and dry ash-free basis for ultimate analysis.

    Parameters
    ----------
    params : dict
        Feedstock parameters.

    Returns
    -------
    ult_bases : dict
        Ultimate analysis bases.
    """

    # as-received basis (% ar)
    ult_ar = params['ultimate_analysis']
    sum_ar = sum(ult_ar)

    # dry basis (% dry)
    ult_dry = [100 * x / (sum_ar - ult_ar[-1]) for x in ult_ar[:-1]]
    sum_dry = sum(ult_dry)

    # dry ash-free basis (% daf)
    ult_daf = [100 * x / (sum_dry - ult_dry[-1]) for x in ult_dry[:-1]]
    sum_daf = sum(ult_daf)

    # dry ash-free C, H, O basis (% daf)
    ult_dafcho = [100 * x / (sum_daf - ult_daf[3] - ult_daf[4]) for x in ult_daf[:-2]]
    sum_dafcho = sum(ult_dafcho)

    # log results to console
    results = (
        f'{" Ultimate analysis ":-^80}\n\n'
        f'             % ar    % dry    % daf    % daf\n'
        f'C        {ult_ar[0]:8} {ult_dry[0]:8.2f} {ult_daf[0]:8.2f} {ult_dafcho[0]:8.2f}\n'
        f'H        {ult_ar[1]:8} {ult_dry[1]:8.2f} {ult_daf[1]:8.2f} {ult_dafcho[1]:8.2f}\n'
        f'O        {ult_ar[2]:8} {ult_dry[2]:8.2f} {ult_daf[2]:8.2f} {ult_dafcho[2]:8.2f}\n'
        f'N        {ult_ar[3]:8} {ult_dry[3]:8.2f} {ult_daf[3]:8.2f}\n'
        f'S        {ult_ar[4]:8} {ult_dry[4]:8.2f} {ult_daf[4]:8.2f}\n'
        f'ash      {ult_ar[5]:8} {ult_dry[5]:8.2f}\n'
        f'moisture {ult_ar[6]:8}\n'
        f'sum      {sum_ar:8.1f} {sum_dry:8.1f} {sum_daf:8.1f} {sum_dafcho:8.1f}\n'
    )

    logging.info(results)

    # return results
    ult_bases = {
        'ar': ult_ar,
        'dry': ult_dry,
        'daf': ult_daf,
        'dafcho': ult_dafcho
    }

    return ult_bases
