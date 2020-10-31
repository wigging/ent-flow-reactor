# Entrained Flow Reactor (EFR)

This repository is for modeling an entrained flow reactor (EFR). The reactor operates at fast pyrolysis conditions to thermochemically convert biomass into gaseous products.

⚠️ This project is being actively developed. Use at your own risk.

## Project structure

**efr** - Python files representing the EFR program.

**params** - Parameter and kinetics files for the EFR program.

## Installation

The EFR program requires the latest version of Python and several packages as listed in the `requirements.txt` file.

## Usage

The EFR program is run from the command line using Python.

```bash
# run the EFR program using the Blend3 feedstock parameters
$ python efr params/blend3.py -em -sp

# use C and H from ultimate analysis to determine biomass composition
$ python efr params/blend3.py --biocomp=ult

# run a batch reactor model and plot the results
$ python efr params/blend3.py -ba -sp

# view all available commands for running the EFR program
$ python efr --help
```

## Contributing

If you would like to contribute code to this project, please submit a Pull Request. Questions, comments, and other feedback can be submitted on the Issues page.
