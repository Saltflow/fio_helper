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