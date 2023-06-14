import os 
filename_timeloop = "timeloop-mapper.stats.txt"
C_name = "Cycles"
filename_gem5 = "/home/gem5/m5out/stats.txt"
T_name = "system.cpu.numCycles"

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


def main():
   # time1 = getCycles(filename_timeloop, C_name, 1)
    time2 = getCycles(filename_gem5, T_name, 0)
   # time_total = time1 + time2
    print("CPU Execution time is :",time2)
   # print("NPU Execution time is :",time1)
    
    #with open('cycle.txt', 'a') as f:
    #    f.write("NPU Execution time is :")
    #    f.write(str(time1))
    #    f.write("\n")
    
    #print("CPU+NPU time consume is :",time_total)

if __name__ == '__main__':
    main()
