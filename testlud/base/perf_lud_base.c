#include<stdio.h>
#include "gemm.h"
#include "../common/common.h"
#define AA(_i,_j) a[_i*size+_j]



void write_input_maxrix_to_file_1(int dim1, int dim2,  int size, float arr[size][size],   const char *filename){
    FILE* fp;
    
    fp = fopen(filename, "w");
    for (int s = 0; s < dim1; s++) {
        if(s == dim1-1 ){
            fprintf(fp, "%f ", arr[dim1][s]);
        }else{
            fprintf(fp, "%f, ", arr[dim1][s]);
        }
    }

    fclose(fp);
}

void write_weight_maxrix_to_file_1(int dim1, int dim2, int size,  float arr[size][size],  const char *filename){
    FILE* fp;
    fp = fopen(filename, "w");
    for (int s = 0; s < dim1; s++) {
        if(s == dim1-1 ){
            fprintf(fp, "%f ", arr[s][dim2]);
        }else{
            fprintf(fp, "%f, ", arr[s][dim2]);
        }
    }

    fclose(fp);
}

void write_input_maxrix_to_file_2(int dim1, int dim2,  int size, float arr[size][size],   const char *filename){
    FILE* fp;

    fp = fopen(filename, "w");
    for (int s = 0; s < dim1; s++) {
        if(s == dim1-1 ){
            fprintf(fp, "%f ", arr[dim2][s]);
        }else{
            fprintf(fp, "%f, ", arr[dim2][s]);
        }
    }

    fclose(fp);
}

void write_weight_maxrix_to_file_2(int dim1, int dim2, int size,  float arr[size][size],  const char *filename){
    FILE* fp;
    fp = fopen(filename, "w");
    for (int s = 0; s < dim1; s++) {
        if(s == dim1-1 ){
            fprintf(fp, "%f ", arr[s][dim1]);
        }else{
            fprintf(fp, "%f, ", arr[s][dim1]);
        }
    }

    fclose(fp);
}



void lud_base(float *a, int size)
{
    float tmp = 0.0;
    int i_h , i_w , w_h, w_w, result;
    //int row = size;
    //int col = size;
    float L[size][size];
    float U[size][size];
    const char *result_file = "/home/gem5/tmp_result/result.txt";
    const char *input_file = "/home/gem5/tmp_result/input.txt";
    const char *weight_file = "/home/gem5/tmp_result/weight.txt";


    for(int p = 0; p < size; p++){
        for (int q =0; q < size; q++){
            if(p == q){
                L[p][q] = 1;
            }
            U[p][q] = 0;
        }
    }
   

    for (int i=0; i<size; i++){
        for (int j=i; j<size; j++){
            if(i == 0){
                U[i][j]=AA(i,j);
            }
            else{
                

		//write_input_maxrix_to_file_1(i ,j, size ,L ,input_file);
                //write_weight_maxrix_to_file_1(i, j ,size ,U ,weight_file);

		/*
                FILE* fp;
                
                fp = fopen("/home/gem5/tmp_result/input.txt", "w");
                for (int s = 0; s < i; s++) {
                    if(s == i-1 ){
                        fprintf(fp, "%f ", L[i][s]);
                    }else{
                        fprintf(fp, "%f, ", L[i][s]);
                    }
                }
                fclose(fp);
               
		
                fp = fopen("/home/gem5/tmp_result/weight.txt", "w");
                for (int s = 0; s < i; s++) {
                    if(s == i-1){
                        fprintf(fp, "%f", U[s][j]);
                    }else{
                        fprintf(fp, "%f,", U[s][j]);
                    }
            
                }
   
                fclose(fp);   
                */ 
               
                /*
                i_h =1 , i_w = i;
		w_h = i, w_w = 1;
		//gemm(i_h,i_w,w_h,w_w);
		
                asm volatile ("iload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h),[b] "r"  (i_w));
                asm volatile ("wload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (w_h), [b] "r"  (w_w));
                asm volatile ("gemm  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h), [b] "r"  (i_w));
                */
             

             
               // tmp  = read_tmp_from_file(result_file);
                tmp = 0.05;
                U[i][j]=AA(i,j) - tmp;
            }
        }

        for (int j=i+1;j<size; j++){
            if(i == 0){
                L[j][i]=AA(j,i)/U[i][i];
            }
            else{

	        
	        /*	    
	        	
                FILE * fp;
   
                fp = fopen("/home/gem5/tmp_result/input.txt", "w");
                for (int s = 0; s < i; s++) {
                    if (s == i-1)
                    {
                        fprintf(fp, "%f", L[j][s]);
                    }
                    else
                    {
                        fprintf(fp, "%f,", L[j][s]);
                    }

                 }
                fclose(fp);


                fp = fopen("/home/gem5/tmp_result/weight.txt", "w");
                for (int s = 0; s < i; s++) {
                    if (s == i-1)
                    {
                        fprintf(fp, "%f", U[s][i]);
                    }
                    else
                    {
                        fprintf(fp, "%f,", U[s][i]);
                    }

                }

                fclose(fp);
                */
		   
		//write_input_maxrix_to_file_2(i, j ,size ,L ,input_file);
                //write_weight_maxrix_to_file_2(i ,j, size ,U ,weight_file);
                
		/* 
                i_h =1 , i_w = i;
		w_h = i, w_w = 1;
		
		asm volatile ("iload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h),[b] "r"  (i_w));
                asm volatile ("wload  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (w_h), [b] "r"  (w_w));
                asm volatile ("gemm  %[c], %[a], %[b];" : [c] "=r" (result) : [a] "r"  (i_h), [b] "r"  (i_w));
		*/
               // gemm(i_h,i_w,w_h,w_w);

             
                tmp = 0.08;
                //tmp  = read_tmp_from_file(result_file);
   
                L[j][i] = (AA(j,i)-tmp)/U[i][i];	     
     
            }
     
        }

    }
    
    /* 
    for (int i = 0;i<size;i++){
        for(int j = 0; j<size;j++){
            printf("%f ",U[i][j]);
        }
        printf("\n");
    }
    for (int i = 0;i<size;i++){
        for(int j = 0; j<size;j++){ 
            printf("%f ",L[i][j]);
        }
        printf("\n");
    }
    */

    
    
}



