#!/usr/bin/env python
#
# C. Bryan Daniels
# bufferize.py
# 2/7/2023
#
# The python package `pint` provides core functionality to this program. It is worth using for any program involving units of all types. https://github.com/hgrecco/pint

import re, csv, argparse
from pathlib import Path
from pint import UnitRegistry

# Instantiate the Units Registry, which create a Quality Constructor, which then parses a 'unit' string
Q = UnitRegistry().Quantity

def is_vol(vol):
    """Is `vol` well formed and having the units of volume.
       '5 ml' is well formed '5' is not """
    try:
        q = Q(vol)
    except:
        return False
    else:
        return q.is_compatible_with('liter')

def is_conc(conc):
    """Is `conc` well formed and having the units of concentration.
       '5 mM', '5 %' and '5x' are well formed. '5 cm' and '5' are not."""
    conc = re.sub(r'x|X|%','', conc)
    try:
        q = Q(conc)
    except:
        return False
    else:
        return q.is_compatible_with('M') or q.is_compatible_with('g/ml') or q.dimensionless

def init_vol(init_conc, final_conc, final_vol):
    """Given the init_conc, final_conc and final_vol,
       returns the required initial volume with appropriate units"""
    init_conc   = re.sub(r'x|X|%','', init_conc) # Allows '%' and "X" in concentrations
    final_conc  = re.sub(r'x|X|%','', final_conc)
    final_vol   = re.sub(r'x|X|%','', final_vol)
    return (Q(final_vol)*Q(final_conc)/Q(init_conc)).to_compact()

def pprint_vol(vol): return(f'{vol:.2f~P}') # Format volume to 2 decimals with short volume units

def make_pathout(reagents_file, final_vol):
    """Convert reagents_file into an pathout"""
    q = Q(final_vol)
    p = Path(reagents_file)
    p = p if p.suffix else p.with_suffix('.csv')
    return Path(f'{p.stem}_{q.m}{q.units:~P}{p.suffix}')

def is_valid_reagents_file(reagents_file):
    with open(reagents_file, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
        if len(set(map(len, lines))) !=1: return False # Check that there 3 elements per line
        for line in lines:
            name, init_conc, final_conc = line
            if not is_conc(init_conc):  return False
            if not is_conc(final_conc): return False
        return True

def formulate_buffer(reagents_file, final_vol, buffer_name, solvent_name):
    """Create the final csv file for output.
        `reagents_file` is a csv file comprised of a `reagent_name`, `init_conc` and `final_conc`
        `final_vol` is the final buffer volume that is being formulated
        `buffer_name` is the name included in the final csv file of the buffer. From the command-line, the default is None
        `solvent_name` is the name solvent used to bring the buffer to the `final_vol`. From the command-line, the default is Water
    """
    if not is_vol(final_vol):
        print(f'final_vol of {final_vol} is not well formed or has wrong units. Sample usage: "200 ml"')
        return
    volume = Q(final_vol)
    if not is_valid_reagents_file(reagents_file):
        print(f'`reagents_file` is not well formed. File should have: 3 elements per line, last 2 being concentrations')
        return
    with open(reagents_file, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
    with open(make_pathout(reagents_file, final_vol), 'w') as file:
        print(f'{buffer_name}\nFinal Volume: {final_vol}', file = file)
        print(f'Reagent,Initial,Final,Volume', file = file)
        for line in lines:
            name, init_conc, final_conc = line
            amount = init_vol(init_conc, final_conc, final_vol)
            volume = volume - amount
            print(f"{name},{init_conc},{final_conc},{pprint_vol( amount)}", file = file)
            print(f"{name},{init_conc},{final_conc},{pprint_vol( amount)}")
        print(f'{solvent_name},,,{pprint_vol(volume)}', file=file)

if __name__ == "__main__":

# Create a Command-line Tool for bufferize.py
    parser = argparse.ArgumentParser(
        prog = 'bufferize',
        description = """
        Formulates a buffer based upon the reagents listed in a a csv file `reagents_file`, with
        three entries per row: `name`, `init_conc` and `final_conc`. The two concentrations need to include
        units of concentrations: uM, mM, M, x or %.
        The `final_volume` is also required. It should include a unit of volume: uL, ml or l.
        Optionally, `buffer_name`, `solvent_name` can be provided.
        The output is a csv file named by appending the final_vol to the original reagents_file.""")


    parser.add_argument('reagents_file', type=str, help="The reagents_file to the csv file" )
    parser.add_argument('final_volume', type=str, help="The total desired amount of buffer. It needs to be a string and must include units." )
    parser.add_argument('--buffer_name',  type=str, help="The name of the buffer. No need for it to be the same as the file.csv" )
    parser.add_argument('--solvent_name', default="Water",  type=str, help="What solvent will be used to bring the buffer to its total volume. Typically water.")

    args = parser.parse_args()
    formulate_buffer(args.reagents_file, args.final_volume, args.buffer_name, args.solvent_name)
