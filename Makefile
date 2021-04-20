TESTS=spdk bdev aio

start:
	python fio_multitest.py --ioengines spdk psync libaio io_uring mmap --test_names $(TESTS) --check_files check_spdk.sh check_kernel.sh check_kernel.sh check_kernel.sh check_kernel.sh

bs:
	python fio_generate.py --ioengine spdk --variable bs spdk.fa
	python fio_generate.py --ioengine psync --variable bs kernel.fa
	python fio_generate.py --ioengine libaio --variable bs aio.fa
	python fio_multitest.py --ioengines spdk psync libaio --test_names $(TESTS) --check_files check_spdk.sh check_kernel.sh check_kernel.sh -a False

bdevtest:
	python fio_multitest.py --ioengines spdk_bdev spdk libaio --test_names $(TESTS) --check_files check_spdk_bdev.sh check_spdk.sh check_kernel.sh

bs:
	python fio_generate.py --ioengine spdk --variable bs spdk.fa
	python fio_generate.py --ioengine spdk_bdev --variable bs bdev.fa
	python fio_generate.py --ioengine libaio --variable bs aio.fa
	python fio_multitest.py --ioengines spdk spdk_bdev libaio --test_names $(TESTS) --check_files check_spdk.sh check_spdk_bdev.sh check_kernel.sh -a False