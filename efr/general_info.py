import logging


def general_info(params):
    """
    Log general information about the program.
    """

    info = (
        f'\n{" General information ":-^80}\n\n'
        f'reactor   = {params.info["reactor_name"]}\n'
        f'feedstock = {params.info["feedstock_name"]}\n'
        f'case      = {params.info["case"]}\n'
    )

    logging.info(info)
