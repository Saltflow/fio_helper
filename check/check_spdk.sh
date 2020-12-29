#! /usr/bash

sudo HUGEMEM=512 ~/spdk/scripts/setup.sh
sudo LD_PRELOAD=~/spdk/build/fio/spdk_nvme fio $1 --output-format=json --output=$2
sudo ~/spdk/scripts/setup.sh reset
