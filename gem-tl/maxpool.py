import torch
from torch import nn

def main():
    with open("/home/gem5/tmp_result/config.txt") as f:
        data = f.readlines()[0:8]
        in_channel = int(data[0])
        in_size = int(data[1])
        out_channel = int(data[2])
        out_size = int(data[3])
        kernel_size = int(data[4])
        layer = int(data[5])
        size = int(data[6])
        stride = int(data[7])

    input = torch.load("/home/gem5/tmp_result/vgg16/input"+str(layer+1)+".pt")
    pool  = nn.MaxPool2d(size , stride=stride)
    out = pool(input)
    torch.save(out, "/home/gem5/tmp_result/vgg16/input"+str(layer+1)+".pt")

if __name__ == '__main__':
    main()

