#! /usr/bash

sudo HUGEMEM=512 ~/spdk/scripts/setup.sh
LD_PRELOAD=~/spdk/build/fio/spdk_nvme sudo fio $1 --output-format=json --output=$2
sudo ~/spdk/scripts/setup.sh reset