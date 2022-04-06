#include <stdio.h>
#include <stdlib.h>

void print_matrix(int rows, int cols, int[rows][cols]);

int main(int argc, char *argv[])
{
    int ret = 0;
    int m[4][2] = {1, 2, 2, 4, 3, 6, 4, 8};
    print_matrix(4, 2, m);

    return ret;
}

void print_matrix(int rows, int cols, int matrix[rows][cols])
{
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            printf("%4d", matrix[r][c]);
        }
        printf("\n");
    }
}
