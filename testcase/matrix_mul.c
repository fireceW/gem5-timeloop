#include <unistd.h>
#include <stdio.h>
#define ROWS 3
#define COLS 3


int main(void)
{
    int a[3][3];
    int b[3][3];
    int array[3][3];
    int result;
    int param1, param2, param3, param4, param5, param6;
    
    //matrix a and b
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            a[i][j] = 1;
            b[i][j] = 3;
        }

    }
    
    //write matrix a and b into file 
    FILE* fp;
    fp = fopen("/home/gem5/tmp_result/input.txt", "w");
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {\
            if (j == COLS - 1 && i == ROWS - 1)
            {
                fprintf(fp, "%d", a[i][j]);
            }
            else
            {
                fprintf(fp, "%d, ", a[i][j]);
            }
        }
    }
    fclose(fp);

    fp = fopen("/home/gem5/tmp_result/weight.txt", "w");
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            if (j == COLS - 1 && i == ROWS - 1)
            {
                fprintf(fp, "%d", b[i][j]);
            }
            else
            {
                fprintf(fp, "%d, ", b[i][j]);
            }

        }
    }
    fclose(fp);

    //Use the extension instruction to pass arguments input_height:3 input_width:3 weight_height:3 weight_width:3
    //Call extension instruction to execute function module(matrix a multiply matrix b)
    param1 = 3 , param2 = 3;
    asm volatile ("iload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (param1),[b] "r"  (param2));
    param3 = 3, param4 = 3;
    asm volatile ("wload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (param3), [b] "r"  (param4));
    param5 = 0, param6 = 0;
    asm volatile ("gemm  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (param5), [b] "r"  (param6));


    //result.txt saves the calculation result
    int found = 0;
    while(!found){
        if (access("/home/gem5/tmp_result/result.txt", F_OK) == 0)
        {   
            found = 1;
            printf("result.txt exists.\n");
	    break;
        }       
    }

    
    return 0;
}

