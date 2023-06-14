# gem5-timeloop

1. update gem5 codes, and complier it

    mv execute.cc gem5/src/cpu/minor/

    mv decoder.isa  gem5/src/arch/riscv/isa/

    scons build/RISCV/gem5.opt -j 64

2. install timeloop(https://timeloop.csail.mit.edu/timeloop)

3. run the lud algorithm(details in run.sh)
   sh run.sh

