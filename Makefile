TESTS=spdk aio nvfuse

start:
	python fio_multitest.py --ioengines spdk psync libaio io_uring mmap --test_names $(TESTS) --check_files check_spdk.sh check_kernel.sh check_kernel.sh check_kernel.sh check_kernel.sh

bs:
	python fio_generate.py --ioengine spdk --variable bs spdk.fa
	python fio_generate.py --ioengine psync --variable bs kernel.fa
	python fio_generate.py --ioengine libaio --variable bs aio.fa
	python fio_multitest.py --ioengines spdk psync libaio --test_names $(TESTS) --check_files check_spdk.sh check_kernel.sh check_kernel.sh -a False

ramtest:
	python fio_multitest.py --ioengines spdk nvfuse_aio libaio --test_names $(TESTS) --check_files check_spdk.sh check_nvfuse.sh check_kernel.sh