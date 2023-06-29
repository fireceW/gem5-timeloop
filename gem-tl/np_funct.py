import argparse
import os
import numpy as np
import sys

  #TODO add other matrix ops
def Load_Funct_Dict():
    funct_dict = {'add':'np.add','sub':'np.subtract'} 
    return funct_dict 


  #getCycles() is used to get cycles from timeloop output
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



    #tl_funct() is used to call timeloop to simulate NPU compute
def tl_funct(instr):
    #Generate the configuration file in timeloop prob from the data in config.txt
    os.system("python ../gem-tl/outgem5_"+instr+".py")
    workspace = "../gtimeloop/"

    prob = workspace + "prob/"+instr+".yaml"
    arch1 = workspace + "arch/components/*.yaml"
    arch2 = workspace + "arch/eyeriss_like.yaml"
    constraints = workspace + "constraints/*.yaml"
    mapper = workspace + "mapper/mapper.yaml"

    cmd = "timeloop-mapper " + prob + " " + arch1 + " " + arch2 +" " + constraints +" " + mapper +" " + "> ../tmp_result/funct.txt 2>&1"
    os.system( cmd )
    
    #Statistics on timeloop output
    filename_timeloop = "timeloop-mapper.stats.txt"
    C_name = "Cycles"

    time = getCycles(filename_timeloop, C_name, 1)  
    
    with open('../tmp_result/cycle.txt', 'a') as f:
        f.write(str(time))
        f.write(",")

   #TODO add more function
def normal_funct(operator):
    with open("../tmp_result/config.txt") as f:
        data = f.readlines()[0:6]
        i_h = int(data[0])
        i_w = int(data[1])
        w_h = int(data[2])
        w_w = int(data[3])

    print("the ops is not implemented now ")

   #gemm_funct() is used to compute matrix mul
   #input weight and matrix size is read from file 
def gemm_funct():
    with open("../tmp_result/config.txt") as f:
        data = f.readlines()[0:6]
        i_h = int(data[0])
        i_w = int(data[1])
        w_h = int(data[2])
        w_w = int(data[3])

    data = np.loadtxt('../tmp_result/input.txt', delimiter=',')
    input = np.resize(data, (i_h,i_w))
    data2 = np.loadtxt('../tmp_result/weight.txt', delimiter=',')
    weight = np.resize(data2, (w_h,w_w))

    result = np.dot(input, weight)
    #result_int = result.astype(np.int8)
    np.savetxt('../tmp_result/result.txt', result, fmt='%.06f',  delimiter=' ')

    if i_w >= 3 :
        tl_funct("gemm")

def numpy_conv(inputs,filter,_result,padding="VALID"):
    H, W = inputs.shape
    filter_size = filter.shape[0]
    # default np.floor
    filter_center = int(filter_size / 2.0)
    filter_center_ceil = int(np.ceil(filter_size / 2.0))

    result = np.zeros((_result.shape))
    H, W = inputs.shape
    for r in range(0, H - filter_size + 1):
        for c in range(0, W - filter_size + 1):
            cur_input = inputs[r:r + filter_size,
                        c:c + filter_size]
            cur_output = cur_input * filter
            conv_sum = np.sum(cur_output)
            result[r, c] = conv_sum
    return result
    #conv_funct() is used to compute conv
def conv_funct():
    with open("../tmp_result/config.txt") as f:
        data = f.readlines()[0:6]
        in_channel = int(data[0])
        in_size = int(data[1])
        weight_channel = int(data[2])
        weight_size = int(data[3])
        stride_size = int(data[4])
        padding = int(data[5])
    
    data = np.loadtxt('../tmp_result/input.txt', delimiter=',')
    input = np.resize(data, (in_channel,in_size,in_size))
    data2 = np.loadtxt('../tmp_result/weight.txt', delimiter=',')
    weight = np.resize(data2, (weight_channel,in_channel,weight_size,weight_size))
    
    C_in, H, W = input.shape
    filter_size = weight.shape[2]
    C_out = weight.shape[0]

    if padding == "VALID":
        result = np.zeros(
            [C_out, int(np.ceil(H - filter_size + 1) / stride_size), int(np.ceil(W - filter_size + 1) / stride_size)],
            np.float32)
    else:
        result = np.zeros([C_out, int(H / filter_size), int(W / filter_size)], np.float32)
        C, H_new, W_new = input.shape
        pad_h = (H_new - 1) * filter_size + filter_size - H
        pad_top = int(pad_h / 2)
        pad_down = pad_h - pad_top

        pad_w = (W_new - 1) * filter_size + filter_size - W
        pad_left = int(pad_w / 2)
        pad_right = pad_w - pad_left
        input = np.pad(input, ((0, 0), (pad_top, pad_down), (pad_left, pad_right)), 'constant',
                        constant_values=(0, 0))
    for channel_out in range(C_out):
        for channel_in in range(C_in):
            channel_data = input[channel_in]
            result[channel_out, :, :] += numpy_conv(channel_data, weight[channel_out][channel_in], result[0],padding)
    
    np.savetxt('../tmp_result/result.txt', result, fmt='%.06f',  delimiter=' ')
    tl_funct("conv")



def main():
   
    parser = argparse.ArgumentParser(description='instr')
    parser.add_argument('arg1', type=str, help='str')
    args = parser.parse_args()

    functdict = Load_Funct_Dict()
    if args.arg1 == "conv":
        conv_funct()    
    elif args.arg1 == "gemm":   
        gemm_funct()
    else:
        normal_funct(functdict[args.arg1])

   # print("NPU Execution time is :",time)
   # elif args.arg1 == "maxpool":
   #     gemm_funct()


if __name__ == '__main__':
    main()


