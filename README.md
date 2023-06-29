# gem5-timeloop

## Environment
   gem5推荐使用docker: docker pull gcr.io/gem5-test/ubuntu-20.04_all-dependencies:v22-1   
   timeloop 参考 http://accelergy.mit.edu/infra_instructions.html

## Operators
1. update gem5 codes, and complier it

    mv execute.cc gem5/src/cpu/minor/

    mv decoder.isa  gem5/src/arch/riscv/isa/

    cd gem5

    scons build/RISCV/gem5.opt -j 64

2. install timeloop(https://timeloop.csail.mit.edu/timeloop)

3. run the lud algorithm(details in run.sh)
   sh run.sh

## Directory
gem-tl: 里面是进行功能运算以及timeloop调用的脚本

&ensp;&ensp;&ensp;&ensp;np_funct.py 进行矩阵的运算(gemm、conv)

&ensp;&ensp;&ensp;&ensp;outgem5_conv.py 根据矩阵的size去设置timeloop模拟卷积运算所需的输入

&ensp;&ensp;&ensp;&ensp;outgem5_conv.py 根据矩阵的size去设置timeloop模拟矩阵乘法运算所需的输入

&ensp;&ensp;&ensp;&ensp;cycle.py 统计cpu和npu的执行时间

gem5:

&ensp;&ensp;&ensp;&ensp; gem5源代码

gtimeloop:

&ensp;&ensp;&ensp;&ensp;timeloop的输入:arch constraints mapper prob，outgem5_conv.py会对prob进行修改。

tmp_result:

&ensp;&ensp;&ensp;&ensp;存放一些文件，包括输入文件(input.txt)、权重文件(weight.txt)等，程序运算时会把矩阵写入到这些文件中去，numpy脚本从文件中读取并进行矩阵运算。

riscv-gnu-chaintool:

&ensp;&ensp;&ensp;&ensp;riscv工具链，在自定义指令时，需要对工具链进行修改。主要修改两个文件riscv-opc.c 和 riscv-opc.h


## Example
 下面这段代码中，内联汇编会把矩阵的size (1,i) (i,1) 通过i_h、i_w、w_h、w_w变量传到指令所用到的寄存器中。然后gem5执行代码时使用的MinorCPU会识别gemm指令，并且获得对应寄存器中的值，然后把矩阵的size写入到config.txt文件中，再执行system("python  ../gem-tl/np_funct.py gemm")。这个python文件会执行具体的卷积运算，并把结果写入到result.txt文件中。同时也会去调用timeloop模型去计算NPU的计算时间。

    program:

    for (int i=0; i<size; i++){
        for (int j=i; j<size; j++){
            if(i == 0){
                U[i][j]=AA(i,j);
            }
            else{
                //把矩阵运算的input写入到文件(tmp_result/input.txt)中
		        write_input_maxrix_to_file_1(i ,j, size ,L ,input_file);
                //把矩阵运算的weight写入到文件(tmp_result/weight.txt)中
                write_weight_maxrix_to_file_1(i, j ,size ,U ,weight_file);
          
                i_h =1 , i_w = i;
		        w_h = i, w_w = 1;
		        //扩展指令 iload 把参数 i_h(input_height) i_w(input_width)传到寄存器中，gem5执行到iload指令时，把i_h 和 i_w 的值(1和i)写入到tmp_result/config.txt中，numpy进行矩阵运算对矩阵进行resize，以及timeloop预测NPU执行时间都需要矩阵的size信息。
                asm volatile ("iload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h),[b] "r"  (i_w));
                asm volatile ("wload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (w_h), [b] "r"  (w_w));
                //gem5执行到gemm指令时，就会并调用numpy脚本读取input.txt weight.txt 以及矩阵的size信息进行执行矩阵操作，并调用timeloop模拟矩阵操作的性能。
                asm volatile ("gemm  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h), [b] "r"  (i_w));
                //程序从tmp_result.txt中读取矩阵运算的结果
                tmp  = read_tmp_from_file(result_file);
               // tmp = 0.05;
                U[i][j]=AA(i,j) - tmp;
            }
        }

        for (int j=i+1;j<size; j++){
            if(i == 0){
                L[j][i]=AA(j,i)/U[i][i];
            }
            else{

		        write_input_maxrix_to_file_2(i, j ,size ,L ,input_file);
                write_weight_maxrix_to_file_2(i ,j, size ,U ,weight_file);
 
                i_h =1 , i_w = i;
		        w_h = i, w_w = 1;
		
		        asm volatile ("iload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h),[b] "r"  (i_w));
                asm volatile ("wload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (w_h), [b] "r"  (w_w));
                asm volatile ("gemm  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h), [b] "r"  (i_w));

                tmp  = read_tmp_from_file(result_file);
   
                L[j][i] = (AA(j,i)-tmp)/U[i][i];	     
            }
        }
    }
    
    gem5/src/cpu/minor/execute.cc:

      if(inst->staticInst->getName() == "gemm"){
           const RegId &reg0 = inst->staticInst->srcRegIdx(0);
           RegVal r0 = thread->getReg(reg0);
           const RegId &reg1 = inst->staticInst->srcRegIdx(1);
           RegVal r1 = thread->getReg(reg1);
           FILE *fp;
           fp = fopen("../tmp_result/config.txt", "a");
           fprintf(fp, "%d\n" ,r0);
           fprintf(fp, "%d\n", r1);
           fclose(fp);
           system("python  ../gem-tl/np_funct.py gemm");

        }


  
