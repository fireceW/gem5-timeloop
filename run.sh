#!/bin/bash

cd gem5

build/RISCV/gem5.opt /home/gem5/configs/example/se.py  --cpu-type=MinorCPU --caches -c ../testlud/base/lud_base  -o"-i ../testlud/tools/10.dat"
build/RISCV/gem5.opt /home/gem5/configs/example/se.py  --cpu-type=MinorCPU --caches -c ../testlud/base/lud_base_perf  -o"-i ../testlud/tools/10.dat"
python ../gem-tl/stat.py
python ../gem-tl/cycle.py
