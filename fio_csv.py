#!/usr/bin/env python3

import argparse
import json
import pprint
import os
import re
import sys

import pandas
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def get_arg_parser():
    p = argparse.ArgumentParser(
        description='Create graphs from various fio json outputs')
    p.add_argument('path', help='Source path for fio output')
    p.add_argument("--bs", "-b", help="list blocksize as variable", type=bool, default=False)
    p.add_argument("--size", "-s", help="list size as variable", type=bool, default=False)
    p.add_argument(
        '-d',
        '--dir', action="store_true",
        help='Read output files from a directory and consider files to be of the same run')
    p.add_argument('-o', '--output', help='output directory for graphs',
                   default='graphs')
    return p


class FioResults(object):

    def __init__(self, args):
        # two parsing modes: single file, dir with files to aggregate
        self.b_width = 0.15
        self.args = args
        self.data = {
            'results': [],
            'directory': self.args.dir
        }
        os.makedirs(self.args.output, exist_ok=True)
        self.cache = {}
        self.meta = {}

    @property
    def num_clients(self):
        if self.meta is {}:
            return 0
        # TODO fix dirty hack
        k = list(self.meta.keys())[0]
        return len(self.meta[k]['clients'])

    @property
    def num_threads(self):
        if self.meta is {}:
            return 0
        # TODO fix dirty hack
        k = list(self.meta.keys())[0]
        return self.meta[k]['count'] / len(self.meta[k]['clients'])

    def parse_data(self):
        if self.args.dir:
            self._parse_dir()
        else:
            self._parse_file(self.args.path)

    def _parse_dir(self):
        for f in os.listdir(self.args.path):
            path = '{}/{}'.format(self.args.path, f)
            if os.path.isfile(path):
                filename = os.path.basename(path)
                self._parse_file(path, filename)

    def _parse_file(self, path, file='default'):
        with open(path) as file_:
            try:
                d = json.load(file_)
                self.data['results'].append(
                    {
                        'name':file ,
                        'stats':d
                    }
                )
            except ValueError:
                print('IGNORING file {}, contains no valid JSON'.format(path))

    def _aggregate_data(self, test): # : tests: self.data['results']
        if not self.data['results']:
            print('ERROR...no data found.')
            sys.exit()

        d = {}
        result = test['stats']
        self.cache['name'] = test['name']
        if 'jobs' in result:
            result_key = 'jobs'
        elif 'client_stats' in result:
            result_key = 'client_stats'

        for job in result[result_key]:
            # Skip 'All clients' if present
            if job['jobname'] == 'All clients':
                continue
            if job['error'] is not 0:
                print('job {} reported an error...skipping'.format(
                    job['jobname']
                ))
                continue
            # Extract data from json
            if job['jobname'] not in d:
                d[job['jobname']] = {'read': 0,
                                        'write': 0,
                                        'r_iops': 0,
                                        'w_iops': 0,
                                        'lat_us': {},
                                        'lat_ms': {},
                                        'clients': [],
                                        'options': {},
                                        'count': 0}
                d[job['jobname']]['options'] = job['job options']

            d[job['jobname']]['count'] += 1
            # if job['hostname'] not in d[job['jobname']]['clients']:
            #     d[job['jobname']]['clients'].append(job['hostname'])
            d[job['jobname']]['read'] += job['read']['bw']
            d[job['jobname']]['write'] += job['write']['bw']
            d[job['jobname']]['r_iops'] += job['read']['iops']
            d[job['jobname']]['w_iops'] += job['write']['iops']
            for k, v in job['latency_us'].items():
                if k in d[job['jobname']]['lat_us']:
                    d[job['jobname']]['lat_us'][k] += job['latency_us'][k]
                else:
                    d[job['jobname']]['lat_us'][k] = job['latency_us'][k]
            for k, v in job['latency_ms'].items():
                if k in d[job['jobname']]['lat_ms']:
                    d[job['jobname']]['lat_ms'][k] += job['latency_ms'][k]
                else:
                    d[job['jobname']]['lat_ms'][k] = job['latency_ms'][k]

        # create data frames from extracted data
        self.cache['bw'] = pandas.DataFrame(data={
            'name': [k for k in d.keys()],
            'read': [v['read'] for v in d.values()],
            'write': [v['write'] for v in d.values()]})
        self.cache['iops'] = pandas.DataFrame(data={
            'name': [k for k in d.keys()],
            'read': [v['r_iops'] for v in d.values()],
            'write': [v['w_iops'] for v in d.values()]})

        lat_data = {'lats': list(d[next(iter(d))]['lat_us'].keys())
                    + [k + '000' for k in d[next(iter(d))]['lat_ms'].keys()]}
        self.cache['meta_clients'] = {k: v['count'] for k, v in d.items()}
        for name in d.keys():
            c = []
            for k in d[name]['lat_us'].keys():
                c.append(d[name]['lat_us'][k] / d[name]['count'])
            for k in d[name]['lat_ms'].keys():
                c.append(d[name]['lat_ms'][k] / d[name]['count'])
            lat_data[name] = c
        self.cache['lat_dist'] = pandas.DataFrame(data=lat_data)

        # collect some metadata about the jobs
        for name in d.keys():
            self.meta[name] = {
                'count': d[name]['count'],
                'clients': d[name]['clients'],
            }

    def get_aggregate_bw(self,test):
        if 'bw' not in self.cache or 'name' != test['name']:
            self._aggregate_data(test)
        return self.cache['bw']

    def get_aggregate_iops(self,test):
        if 'iops' not in self.cache or 'name' != test['name']:
            self._aggregate_data(test)
        return self.cache['iops']

    def get_aggregate_lat_dist(self,test):
        if 'lat_dist' not in self.cache  or 'name' != test['name']:
            self._aggregate_data(test)
        return self.cache['lat_dist']

    def print_(self):
        mergedbw = 0
        mergediops = 0
        for test in self.data['results']:
            print('aggregate iops')
            ag_iops = self.get_aggregate_iops(test)
            ag_iops['way'] = attach_name(test['name'], ag_iops.shape[0])
            print('aggregate bandwidth')
            ag_bw = self.get_aggregate_bw(test)
            ag_bw['way'] = attach_name(test['name'], ag_bw.shape[0])
            if(type(mergedbw) == int): # tricks to get accumulated result
                mergedbw = ag_bw.copy()
                mergediops = ag_iops.copy()
            else:
                mergedbw = mergedbw.append(ag_bw)
                mergediops = mergediops.append(ag_iops)
        print("merged!!")
        with pandas.ExcelWriter("file.xlsx") as writer:
            mergedbw.to_excel(writer, sheet_name='bw')
            mergediops.to_excel(writer, sheet_name='iops')


def attach_name(name, number):
    result = []
    for i in range(number):
        result.append(name)
    return result

def get_workers(val):
    return 0

def get_bs(val):
    return 0

def get_op(val):
    return val.split('_')[-1]


def get_fio(path):
    return FioResults(argparse.Namespace(dir=True, path=path, output='graphs'))


def main():
    a_parser = get_arg_parser()
    args = a_parser.parse_args()

    if args.dir:
        if not os.path.isdir(args.path):
            raise a_parser.ArgumentError(('-d was passed but path is not a ',
                                         'directory'))
    else:
        if os.path.isdir(args.path):
            raise a_parser.ArgumentError(('-d was not passed but path is a ',
                                         'directory'))

    results = FioResults(args)
    results.parse_data()
    results.print_()


if __name__ == "__main__":
    main()
