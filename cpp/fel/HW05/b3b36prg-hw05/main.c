#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void print_matrix(int rows, int cols, int[rows][cols]);

_Bool check_matrix_dim(int *r, int *c);
_Bool read_matrix(int rows, int cols, int[rows][cols]);

enum { ERROR_INPUT = 100 };

int main(int argc, char *argv[])
{
    int ret = 0;
    int row1, col1;
    row1 = col1 = 1;
    if (check_matrix_dim(&row1, &col1))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    int m1[row1][col1];
    if (ret == EXIT_SUCCESS && read_matrix(row1, col1, m1))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    if (ret == ERROR_INPUT)
        fprintf(stderr, "Error: Chybny vstup!\n");

    if (ret == EXIT_SUCCESS) {
        print_matrix(row1, col1, m1);
    }
}

void print_matrix(int rows, int cols, int matrix[rows][cols])
{
    fprintf(stderr, "Dims: %d x %d\n", rows, cols);
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
    _Bool ret;
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            if (scanf("%d", &(matrix[r][c])) == 1) {
                ret = true;
            } else
                ret = false;
        }
    }
    return ret;
}