#!/usr/bin/env bash

sudo HUGEMEM=64 bash ~/fio/spdk/scripts/setup.sh
sudo LD_PRELOAD=/home/vagrant/fio/spdk/build/fio/spdk_nvme fio $1 --output-format=json --output=$2
sudo sh ~/fio/spdk/scripts/setup.sh reset