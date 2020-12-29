#! /usr/bash
sudo mkfs.ext4 /dev/nvme0n1
sudo mount -t ext4 -F /dev/nvme0n1 /nvmedir
sudo fio $1 --output-format=json --output=$2