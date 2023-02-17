# bufferize
# Formulate Chemical and Biological Buffers from Reagents

#### Developed by C. Bryan Daniels
Though I've tested `bufferize` for my own purposes. Please double check that its results seem reasonable. Feel free to contact me with issues, suggestions or questions at cdaniels@uchicago.edu

### Overview
The idea behind `bufferize.py` is to make it easy to formulate buffers. Protocols often stipulate the final concentrations of reagents, but don't give the actual recipe to mix the buffers since the protocol authors are not aware of the stock concentrations in a specific lab. Once the stock concentrations are known, it is not difficult to then formulate the buffers. It is however, tedious and error-prone, which is what `bufferize.py` attempts to do.

```
bufferize -h
usage: bufferize [-h] [--buffer_name BUFFER_NAME] [--solvent_name SOLVENT_NAME] reagents_file final_volume

Formulates a buffer based upon the reagents listed in a a csv file `reagents_file`, with three entries 
per row: `name`, `init_conc` and `final_conc`. The two concentrations need to include units of 
concentrations: uM, mM, M, x or %. The `final_volume` is also required. It should include a unit 
of volume: uL, ml or l. Optionally, `buffer_name`, `solvent_name` can be provided. The output is 
a csv file named by appending the final_vol to the original reagents_file.

positional arguments:
  reagents_file         The reagents_file to the csv file
  final_volume          The total desired amount of buffer. It needs to be a string and must include units.

options:
  -h, --help            show this help message and exit
  --buffer_name BUFFER_NAME
                        The name of the buffer. No need for it to be the same as the file.csv
  --solvent_name SOLVENT_NAME
                        What solvent will be used to bring the buffer to its total volume. Typically water.        
```

### Installation
Requires Python 3+
``` 
pip install pint
git clone https://github.com/prairie-guy/bufferize.git
```
### Usage
To use `bufferize` you will need to decide how much of the final buffer you will need. Also required is a `reagents.csv` file that includes the name of the reagents, its stock concentration and the final concentration. Units of concentration need to be provided: mM, M, g/ml, %, X etc.

The script does basic error checking, but the requirements for the `reagents.csv` file are:
- CSV format, i.e, Comma Separated Values. Quotes are not needed. Do not use a comma except to separate elements.
- Do not use a header, i.e., do NOT include a line similar to `name`, `initial`, `final` at the top of the `reagents.csv` file.
- Each line needs to have exactly three elements separated by a single comma: `name of reagent` (a string), `initial_conc` and `final_conc` (for both a number followed by a unit of concentration: mM, M, g/ml, %, X,etc). All other units will fail.
- All the traditional modifications of units (or their abbreviations) are recognized: pico, nano, micro, milli, kilo, etc.
- Here is an example line: EDTA pH 7.4, 1M, 2.5 mM
- Note that for concentrations, spacing between the number and its unit is optional
- When using `%` or `X`, be sure to use the same unit for `initial_conc` and `final_conc`

In addition to the `reagents.csv`file, when running the program, you must stipulate the `final_volume`. Optionally, you can include the `buffer_name` (which will be included in the final output, which will be another csv file. Also optional are the `solvent`, which by default is `water`.

The required volume of solvent (water by default) is included in the final csv file.

The output will be a new csv file named by appending the `final_volume` to the name of the `reagents.csv` file name.

For properly formatting the new csv file, use Excel, Numbers or an other program.

**Note: At the present, `bufferize.py` and the `reagents.csv` file must be located in the same directory.**

### Example
```
python bufferize.py SDS_lysis_buffer.csv "200 ml" --buffer_name "SDS Buffer" --solvent "DNase Free H20"
```

```Input CSV File: SDS_lysis_buffer.csv```

```
Tris-HCl pH7.5  1M    10mM
NaCl            5M    150mM
EDTA            500mM 1mM
Triton X-100    10%   1%
SDS             10%   0.10%
```

```Output CSV File: SDS_lysis_buffer_200ml.csv```

```
SDS Buffer			
Final Volume: 200 ml			
Reagent         Initial Final Volume
Tris-HCl pH7.5  1M      10mM  2.00 ml
NaCl            5M      150mM 6.00 ml
EDTA            500mM   1mM   400.00 µl
Triton X-100    10%     1%    20.00 ml
SDS             10%     0.10% 2.00 ml
DNase Free H20                169.60 ml
```
#### Attribution
The core functionality of `bufferize` is provided by the python package `pint` https://github.com/hgrecco/pint, which enable simple unit conversions. It has much more functionality than I've utilized here. It is worth checking out if you are doing anything related units or all types. 


