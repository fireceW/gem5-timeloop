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
        layer = int(data[5])

    weight = torch.load("/home/gem5/tmp_result/vgg16/weight"+str(layer)+".pt")
    input_ = torch.load("/home/gem5/tmp_result/vgg16/input"+str(layer)+".pt")
    bias = torch.load("/home/gem5/tmp_result/vgg16/bias"+str(layer)+".pt")

    input = torch.reshape(input_,(1,i_h))

    m = nn.Linear(i_h,w_w)
    m.weight=nn.Parameter(weight)
    m.bias = nn.Parameter(bias)

    out = m(input)
    torch.save(out, "/home/gem5/tmp_result/vgg16/input"+str(layer+1)+".pt")

    # Call timeloop for performance statistics
    tl_funct("gemm")

def conv_funct():
    with open("/home/gem5/tmp_result/config.txt") as f:
        data = f.readlines()[0:6]
        in_channel = int(data[0])
        in_size = int(data[1])
        out_channel = int(data[2])
        out_size = int(data[3])
        kernel_size = int(data[4])
        layer = int(data[5])
    print(layer)
    weight = torch.load("/home/gem5/tmp_result/vgg16/weight"+str(layer)+".pt")
    input = torch.load("/home/gem5/tmp_result/vgg16/input"+str(layer)+".pt")
    bias = torch.load("/home/gem5/tmp_result/vgg16/bias"+str(layer)+".pt")


    conv = nn.Conv2d(in_channels = in_channel, out_channels = out_channel, kernel_size = kernel_size, padding = 1)
    conv.weight = nn.Parameter(weight)
    conv.bias = nn.Parameter(bias)
    
    relu = nn.ReLU(inplace=True)
    imm  = conv(input)
    out  = relu(imm)
    torch.save(out, "/home/gem5/tmp_result/vgg16/input"+str(layer+1)+".pt")

    tl_funct("conv")



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


