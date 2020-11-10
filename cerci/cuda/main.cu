#include "tensoroperations.cuh"

#include <iostream>
#include <stdlib.h>

int main() {

    int size1 = 1 << 4;
    int dim_size1 = 3;
    std::unique_ptr<int[]> dims1(new int[dim_size1]{4, 2, 2});
    std::unique_ptr<float[]> mat1(new float[size1]);
    for (int i = 0; i < size1; i++) {
        mat1[i] = rand() % 4;
    }

    // int size2 = 1 << 3;
    // int dim_size2 = 3;
    // std::unique_ptr<int[]> dims2(new int[dim_size1]{2, 2, 2});
    // std::unique_ptr<float[]> mat2(new float[size1]);
    // for (int i = 0; i < size2; i++) {
    //     mat2[i] = rand() % 4;
    // }

    // Nothing is being returned
    int dupe_size = 3;
    std::unique_ptr<float[]> out_mat = CUDAdupe(mat1, dims1, dim_size1, size1, dupe_size); // This isnt doing the full dupe only returns zeros

    std::cout << std::endl;
    for (int i = 0; i < size1 * dupe_size; i++) {
        std::cout << out_mat[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}