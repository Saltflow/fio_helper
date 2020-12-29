<<<<<<< HEAD
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
=======
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
        description='Create automated comparation for multiple ioengines, ioengines, test name and checkfiles should be strictly one-to-one')
    p.add_argument('--base_file', "-b", help='the base for fio test',default='default.fio')

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
    ioengine,check,test,base = args
    for i in range(len(ioengine)):
        os.system("python fio_generate.py --base=" + base + " " + "--ioengine=" + ioengine[i] + " " +
        test[i] + ".fa")


def run_fio_test(args):
    try:
        os.makedirs("test_result")
    except Exception as exc:
        print("test_result already exist or failed")
        print(exc)
    __,check,test,__ = args
    for i in range(len(check)):
        cmd = "bash ./check/" + check[i] + " " + "./" + test[i] + ".fa" + " ./test_result/" + test[i]
        print("Running " + cmd)
        os.system(cmd)
        
def merge_fio_result(args):
    os.system("python fio_csv.py -d ./test_result/ result.xlsx")

def clear_amid(args):
    pass

def ns2list(ns):
    olist = []
    for i in ns:
        olist.append(i)
    return olist


def main():
    args = get_arg_parser().parse_args()
    ioengine = ns2list(args.ioengines)
    check = ns2list(args.check_files)
    test = ns2list(args.test_names)
    base = args.base_file
    arg = (ioengine, check, test, base)
    genetare_fio_file(arg)
    run_fio_test(arg)
    merge_fio_result(arg)
    

if __name__ == "__main__":
>>>>>>> 975fe35d4f55d8759a5fdec57dcfa45d1e7395fa
    main()