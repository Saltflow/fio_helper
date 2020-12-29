#!/usr/bin/env python3
import argparse
import json
import os
import sys

'''''
Generate multiple testcases and run them sequentially via fio

'''''
def get_arg_parser():
    p = argparse.ArgumentParser(
        description='Create automated comparation for multiple ioengine')
    p.add_argument('base_file', help='the base for fio test',default='default.fio')

    p.add_argument("--ioengines", "-g", help="ioengines", type=str, nargs='+')
    p.add_argument("--test_names", "-t", help="test names on diffrent ioengines", type=str, nargs='+')
    p.add_argument("--check_files", "-c", help="check files(do mounting fs, clearing cache, etc.) to prepared for fio test",
    type=str, nargs='+')
    return p

def genetare_fio_file(args):
    try:
        os.makedirs("fio_file")
    except:
        print("fio_file already exist")
    for i in range(len(args.ioengines)):
        os.system("python fio_generate.py --base=" + args.base_file + " " + "--ioengine=" + args.ioengines[i] + " " +
        args.test_names[i])


def run_fio_test(args):
    try:
        os.makedirs("test_result")
    except:
        print("test_result already exist")
    for i in range(len(args.check_files)):
        os.system("sh ./check/" + 
        args.check_files[i] + " " + args.test_names[i] + "./test_result/" + args.test_names[i])
        
def merge_fio_result(args):
    os.system("python fio_csv.py -d ./test_result/ result.xlsx")

def clear_amid(args):
    pass

def main():
    args = get_arg_parser()
    genetare_fio_file(args)
    run_fio_test(args)
    merge_fio_result(args)
    

if __name__ == "__main__":
    main()