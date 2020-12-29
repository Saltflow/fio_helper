#! /usr/bash
echo "using spec file $1 to the result $2"
sudo mkfs.ext4 -t ext4 -F /dev/nvme0n1
sudo mount -t ext4 -F /dev/nvme0n1 /nvmedir
sudo fio $1 --output-format=json --output=$2
umount /nvmedir