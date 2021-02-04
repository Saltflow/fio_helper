#!/usr/bin/env bash

echo "using spec file $1 to the result $2"
sudo mount -t ramfs -o size=1024m -F ramfs /nvmedir
sudo fio $1 --output-format=json --output=$2
sudo umount /nvmedir