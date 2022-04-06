#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void print_matrix(int rows, int cols, int[rows][cols]);

_Bool check_matrix_dim(int *r, int *c);
_Bool read_matrix(int rows, int cols, int[rows][cols]);

int main(int argc, char *argv[])
{
    int ret = 0;
    int row1, col1, row2, col2;
    row1 = col1 = 1;
    if (!check_matrix_dim(&row1, &col1)) {
        fprintf(stderr, "ERROR DIM OF MATRIX\n");
        ret = 101;
    }
    int m1[row1][col1];
    if (ret == 0 && !read_matrix(row1, col1, m1)) {
        fprintf(stderr, "ERROR READ OF MATRIX\n");
        ret = 102;
    }
    if (ret == 0) {
        print_matrix(row1, col1, m1);
    }

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

_Bool check_matrix_dim(int *r, int *c)
{
    _Bool ret;
    if (scanf("%d %d", r, c) == 2) {
        ret = true;
    } else {
        ret = false;
    }
    return ret;
}

_Bool read_matrix(int rows, int cols, int matrix[rows][cols])
{
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            if (scanf("%d", &(matrix[r][c])) != 1) {
                return false;
            }
        }
    }
    return true;
}