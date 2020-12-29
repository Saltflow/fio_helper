# fio_graphs
Plot fio results with matplotlib.

## Notes

* tries to remain agnostic to your actual jobs
* aggregates on job name; i.e. aggregates job duplication with numjobs and
  aggregates across multiple client nodes if the sam job file is used with fio's
  client/server mode

## Requirements
Requires python libraries

* matplotlib
* pandas
* numpy

# Running
Run ``./fio_plots.py --help``

## Design doc

一共分两部分：

fio测试文件生成、fio结果文件解析

fio测试文件生成：

1. 设置好测试的global参数 ————不用设置，默认参数一套

2. 规定上界下界和测试点数量，按照某一规则（线性、指数、对数）对某一个变量生成一组测试数据

3. 自动生成命名和description

需要注意的问题：

1. iodepth和size,bs的默认不太相同

2. bs的合法性

step固定为2,一个加算一个乘算，对数删掉

解析主要解析为：

测试变量，读速度、写速度

测试变量，读IOPS，写IOPS

(xlsx的话两个合一个文件，不同的sheet)

测试变量主要支持：

size,bs,iodepth

