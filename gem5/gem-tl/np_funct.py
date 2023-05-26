import torch
from torch import nn
import os
import sys

def getCycles(filename, stringName, timeloop_flag):
    with open(filename, "r")as f:
        for line in f:
            if stringName in line:
                if timeloop_flag:
                    num = line.split(":")[1].split(" ")[1]
                    return int(num)
                else:
                    num = line.split("#")[0].split("system.cpu.numCycles")[1]
                    return int(num)


def tl_funct(instr):
    #Generate the configuration file in timeloop prob from the data in config.txt
    os.system("python /home/gem5/gem-tl/outgem5_"+instr+".py")
    workspace = "/home/yangnan/gtloopg/gtimeloop/"

    prob = workspace + "prob/"+instr+".yaml"
    arch1 = workspace + "arch/components/*.yaml"
    arch2 = workspace + "arch/eyeriss_like.yaml"
    constraints = workspace + "constraints/*.yaml"
    mapper = workspace + "mapper/mapper.yaml"

    cmd = "timeloop-mapper " + prob + " " + arch1 + " " + arch2 +" " + constraints +" " + mapper +" " + "> tmp_result/funct.txt 2>&1"
    os.system( cmd )

    #Statistics on timeloop output
    filename_timeloop = "timeloop-mapper.stats.txt"
    C_name = "Cycles"
   # filename_gem5 = "/home/gem5/m5out/stats.txt"
   # T_name = "system.cpu.numCycles"

    time = getCycles(filename_timeloop, C_name, 1)
    print("NPU Execution time is :",time)

    with open('cycle.txt', 'a') as f:
        f.write("NPU Execution time is :")
        f.write(str(time))
        f.write("\n")


def gemm_funct():
    with open("/home/gem5/tmp_result/config.txt") as f:
        data = f.readlines()[0:6]
        i_h = int(data[0])
        i_w = int(data[1])
        w_h = int(data[2])
        w_w = int(data[3])

    data = np.loadtxt('/home/gem5/tmp_result/input.txt', delimiter=',')
    input = np.resize(data, (i_h,i_w))
    data2 = np.loadtxt('/home/gem5/tmp_result/weight.txt', delimiter=',')
    weight = np.resize(data2, (w_h,w_w))

    result = np.dot(input, weight)
    result_int = result.astype(np.int8)
    np.savetxt('/home/gem5/tmp_result/result.txt', result, fmt='%d',  delimiter=' ')

    if w_h<= 5 and w_w == 1 :
        print("timeloop's bug and do not know how to deal with it")
    else:
        tl_funct("gemm")

def conv_funct():
    print("The ability to use numpy for convolution is not yet implemented")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='instr')
    parser.add_argument('arg1', type=str, help='str')
    args = parser.parse_args()
    if args.arg1 == "conv":
        conv_funct()    
    elif args.arg1 == "gemm":   
        gemm_funct()
   # elif args.arg1 == "maxpool":
   #     gemm_funct()


if __name__ == '__main__':
    main()


