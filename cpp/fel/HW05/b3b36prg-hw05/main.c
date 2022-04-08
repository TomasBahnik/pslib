#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void print_matrix(int rows, int cols, int[rows][cols]);
bool sum(int rows1, int cols1, int matrix1[rows1][cols1], int rows2, int cols2,
         int matrix2[rows2][cols2], int rows3, int cols3,
         int matrix3[rows3][cols3], int sign);

bool check_matrix_dim(int *r, int *c);
bool read_matrix(int rows, int cols, int[rows][cols]);

enum { ERROR_INPUT = 100 };

int main(int argc, char *argv[])
{
    int ret = 0;
    // loading matrix 1
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

    // loading char between matrix 1 and 2
    char op[2];
    if ((scanf("%1s", op)) != 1 ||
        (op[0] != '+' || op[0] != '-' || op[0] != '*'))
        ret = ERROR_INPUT;
    else
        ret = EXIT_SUCCESS;

    // loading matrix 2
    int row2, col2;
    row2 = col2 = 1;
    if (check_matrix_dim(&row2, &col2))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    int m2[row2][col2];
    if (ret == EXIT_SUCCESS && read_matrix(row2, col2, m2))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;

    if (ret == ERROR_INPUT)
        fprintf(stderr, "Error: Chybny vstup!\n");

    if (ret == EXIT_SUCCESS) {
        print_matrix(row1, col1, m1);
        printf("symbol: %s\n", op);
        print_matrix(row2, col2, m2);
    }
    int sign = 1;
    switch (op[0]) {
    case '-':
        sign = -1;
    case '+': {
        int result[row1][col1];
        sum(row1, col1, m1, row2, col2, m2, row1, col1, result, sign);
        print_matrix(row1, col1, result);
    } break;

    default:
        break;
    }
    return ret;
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

bool check_matrix_dim(int *r, int *c)
{
    _Bool ret;
    if (scanf("%d %d", r, c) == 2) {
        ret = true;
    } else {
        ret = false;
    }
    return ret;
}

bool read_matrix(int rows, int cols, int matrix[rows][cols])
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

bool sum(int rows1, int cols1, int matrix1[rows1][cols1], int rows2, int cols2,
         int matrix2[rows2][cols2], int rows3, int cols3,
         int matrix3[rows3][cols3], int sign)
{
    if (rows1 == rows2 && cols1 == cols2 && rows1 == rows3 && cols1 == cols3) {
        for (int r = 0; r < rows1; ++r) {
            for (int c = 0; c < cols1; ++c) {
                matrix3[r][c] = matrix1[r][c] + sign * matrix2[r][c];
            }
        }
        return true;
    } else
        return false;
}