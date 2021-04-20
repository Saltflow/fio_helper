#!/usr/bin/env python3

import argparse
import json
import pprint
import os
import sys

globalattr="""
[global]
thread=1
group_reporting=1
direct=1
verify=0
time_based=1
ramp_time=0
runtime=30
bs=4k
size=4m
iodepth=4
rw=rw
"""

def decide_initial(args):
    global globalattr
    if(args.base != "default.fio"):
        with open(args.base, 'r') as f:
            attrs = f.readlines()
            globalattr = '\n'.join(attrs)
    if(args.ioengine!="spdk"):
        filename_s = "filename=/nvmedir/hello\n"
    else:
        filename_s = "filename=trtype=PCIe traddr=0000.00.0e.0 ns=1\n"
    if(args.ioengine=="spdk_bdev"):
        filename_s = "spdk_conf=/home/vagrant/fio_helper/nvme.conf\n"
    globalattr += "ioengine=" + args.ioengine + "\n"
    globalattr += filename_s + '\n'

def generate_points(args):
    min_num = 0
    max_num = 0
    factor = 2
    if(args.variable != "iodepth"):
        min_num = pow(2,12)
        max_num = pow(2,22)
        factor = 512
    else:
        min_num = 8
        max_num = pow(2,9)
    generated = []
    generated.append(min_num)

    for i in range (args.test_count):
        if(args.exponential):
            generated.append(generated[i] * 2)
        else:
            generated.append(generated[i] + (max_num - min_num) //10 // factor * factor)
        if(generated[i] > max_num):
            break
    return generated



def get_arg_parser():
    p = argparse.ArgumentParser(
        description='Create fio file for various input')
    p.add_argument('fioname', help='Source name for fio output',default='generated.fio')

    p.add_argument("--linear", "-l", help="linear output", type=bool, default=True)
    p.add_argument("--exponential", "-e", help="genetare exp output", type=bool, default=False)

    p.add_argument("--test_count", "-c", help="number of test set", type=int, default=10)
    p.add_argument("--start", "-s", help="start number", type=int, default=4096)
    p.add_argument("--variable", "-v", help="""possible vagriable,
    `size` `bs` `iodepth` is supported now, note different variable should have different defalut value
    """, type=str, default="size")
    p.add_argument("--ioengine", "-g", help="what ioengine", type=str, default="psync")
    p.add_argument("--base", help="global attr for fio", type=str, default="default.fio")
    return p

def main():
    global globalattr
    a_parser = get_arg_parser()
    args = a_parser.parse_args()
    with open(args.fioname,"w") as f:
        decide_initial(args)
        f.write(globalattr)
        data_all = generate_points(args)
        for data in data_all:
            f.write('['+ args.variable + "=" + str(data) + ']\n')
            f.write("stonewall\n")
            f.write('description=\"'+ "variable " + args.variable +  '\"\n')
            f.write(args.variable + "=" + str(data) +"\n\n")




if __name__ == "__main__":
    main()
