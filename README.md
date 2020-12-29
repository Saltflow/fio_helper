# fio_graphs
Parse fio results to xlsx.

## Notes



## Requirements
Requires python libraries

* pandas
* numpy


---

## Running

### Simple way

Run `fio_multitest.py -h`, fill the check file in `check`, designate `ioengine` and the name of the test

## Scripts

### fio_csv.py

The main script for parsing the fio file and exported to `.xlsx` file,
note it is easy to modify it into `.csv` file

### fio_generate.py

Generate test cases by given variable, ioengine, etc.

### ./check

The `.sh` scripts for actually launch `fio`. Running an fio may have a lot to do beforehead, as well as clean the settings afterward, such as mounting a fs, loading a plugin, etc. In convenience to be called by `fio_multitest`, the first two arguments need to be input and output file for `fio`

### fio_multitest.py

Merge everything together.Generating test cases, running them via chekcfile,then convert the data via `fio_csv.py`