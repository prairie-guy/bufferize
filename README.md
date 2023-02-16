# bufferize
Formulate Chemical and Biological Buffers from Reagents

The idea for `bufferize.py` is to make it easy to formulate buffers. Protocols often stipulate the final concentrations of reagents, but don't give the actual recipe to mix the buffers, as the protocol authors are not aware of the stock concentrations in a specific lab. Once the stock concentrations are known, it is not difficult to then formulate the buffers. It is however, tedious and error-prone. That is the purpose of `bufferize.py`


```
bufferize -h
usage: bufferize [-h] [--buffer_name BUFFER_NAME] [--solvent_name SOLVENT_NAME] reagents_file final_volume

Formulates a buffer based upon the reagents listed in a a csv file `reagents_file`, with three entries per row: `name`, `init_conc` and `final_conc`. The two concentrations need to include units of
concentrations: uM, mM, M, x or %. The `final_volume` is also required. It should include a unit of volume: uL, ml or l. Optionally, `buffer_name`, `solvent_name` can be provided. The output is a csv file
named by appending the final_vol to the orginal reagents_file.

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

