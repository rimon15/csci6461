/**
 * In this program, we test massive parallel threading via cuda, and compare it to 
 * the single-threaded host only code. We see that the massive parallelization for matrix multiplication
 * gives us an immense boost in compute time on the GPU as opposed to host only.
*/

#include <stdio.h>
#include <time.h>


const int DSIZE = 512 * 2;
const int block_size = 16;  // CUDA maximum is 1024 total threads in block
const float A_val = 1.0f;
const float B_val = 2.0f;

// matrix multiply kernel: C = A * B
__global__ void mmul(const float *A, const float *B, float *C, int ds) {

  int idx = threadIdx.x+blockDim.x*blockIdx.x; // create thread x index
  int idy = threadIdx.y+blockDim.y*blockIdx.y; // create thread y index

  if ((idx < ds) && (idy < ds)){
    float temp = 0;
    for (int i = 0; i < ds; i++)
      temp += A[idx*ds+i] * B[i*ds+idy];   // dot product of row and column
    C[idy*ds+idx] = temp;
  }
}

int main(){

    float *h_A, *h_B, *h_C, *d_A, *d_B, *d_C;

    // these are just for timing
    clock_t t0, t1, t2;
    double t1sum=0.0;
    double t2sum=0.0;

    // start timing
    t0 = clock();

    h_A = new float[DSIZE*DSIZE];
    h_B = new float[DSIZE*DSIZE];
    h_C = new float[DSIZE*DSIZE];
    for (int i = 0; i < DSIZE*DSIZE; i++){
        h_A[i] = A_val;
        h_B[i] = B_val;
        h_C[i] = 0;
    }

    // Initialization timing
    t1 = clock();
    t1sum = ((double)(t1-t0))/CLOCKS_PER_SEC;
    printf("Init took %f seconds.  Begin compute\n", t1sum);

    // Allocate device memory and copy input data over to GPU
    cudaMalloc(&d_A, DSIZE*DSIZE*sizeof(float));
    cudaMalloc(&d_B, DSIZE*DSIZE*sizeof(float));
    cudaMalloc(&d_C, DSIZE*DSIZE*sizeof(float));
    cudaMemcpy(d_A, h_A, DSIZE*DSIZE*sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, DSIZE*DSIZE*sizeof(float), cudaMemcpyHostToDevice);

    // Cuda processing sequence step 1 is complete

    // Launch kernel
    dim3 block(block_size, block_size);  // dim3 variable holds 3 dimensions
    dim3 grid((DSIZE+block.x-1)/block.x, (DSIZE+block.y-1)/block.y);
    mmul<<<grid, block>>>(d_A, d_B, d_C, DSIZE);

    // Cuda processing sequence step 2 is complete

    // Copy results back to host
    cudaMemcpy(h_C, d_C, DSIZE*DSIZE*sizeof(float), cudaMemcpyDeviceToHost);

    // GPU timing
    t2 = clock();
    t2sum = ((double)(t2-t1))/CLOCKS_PER_SEC;
    printf ("Done. Compute took %f seconds\n", t2sum);

    // Cuda processing sequence step 3 is complete

    // Verify results, and compare with the host only results.
    for (int i = 0; i < DSIZE*DSIZE; i++) if (h_C[i] != A_val*B_val*DSIZE) {
        printf("mismatch at index %d, was: %f, should be: %f\n", i, h_C[i], A_val*B_val*DSIZE); return -1;
    }
    printf("Success!\n"); 

    clock_t t3 = clock();
    for (int i = 0; i < DSIZE; i++) {
        for (int j = 0; j < DSIZE; j++) {
            for (int k = 0; k < DSIZE; k++) {
                h_C[i * j] += h_A[i * k] * h_B[j * k];
            }
        }
    }
    clock_t t4 = clock();
    double t4sum = ((double)(t4-t3))/CLOCKS_PER_SEC;
    printf ("Done. CPU Compute took %f seconds\n", t4sum);
    return 0;
}
  
