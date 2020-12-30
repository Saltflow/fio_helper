TESTS=spdk kernel

start:
	python fio_multitest.py --ioengines spdk psync --test_names $(TESTS) --check_files check_spdk.sh check_kernel.sh