#!/usr/bin/env bash

echo "using spec file $1 to the result $2"
sudo HUGEMEM=4096 ~/spdk/scripts/setup.sh
sudo LD_PRELOAD=~/spdk/build/fio/spdk_bdev fio $1 --output-format=json --output=$2
sudo ~/spdk/scripts/setup.sh reset
