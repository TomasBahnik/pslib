#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

int load_input(int r1, int c1, int r2, int c2);

// work with matrix
void print_matrix(int rows, int cols, int[rows][cols]);
bool check_matrix_dim(int *r, int *c);
bool read_matrix(int rows, int cols, int[rows][cols]);

// operations
bool sum(int r1, int c1, int m1[r1][c1], int r2, int c2, int m2[r2][c2], int r3,
         int c3, int m3[r3][c3], int sign);
bool multi(int r1, int c1, int m1[r1][c1], int r2, int c2, int m2[r2][c2],
           int m3[r1][c2], int sign);

// output value
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
        (op[0] != '+' || op[0] != '-' ||
         op[0] != '*')) //<--- TODO - if condiotin never happend
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

    // if (ret == EXIT_SUCCESS) {
    //     print_matrix(row1, col1, m1);
    //     printf("symbol: %s\n", op);
    //     print_matrix(row2, col2, m2);
    // }
    int sign = 1;
    int sum_res[row1][col1];
    int mul_res[row1][col2];
    switch (op[0]) {
    case '-': // inversion to sum function
        sign = -1;
    case '+': { // sum function
        sum(row1, col1, m1, row2, col2, m2, row1, col1, sum_res, sign);
        print_matrix(row1, col1, sum_res);
    } break;
    case '*':
        multi(row1, col1, m1, row2, col2, m2, mul_res, sign);
        print_matrix(row1, col2, mul_res);
    default:
        ret = ERROR_INPUT;
        break;
    }
    return ret;
}
// TODO, only if its necesery (can be deleted)
int load_input(int r1, int c1, int r2, int c2)
{
    int ret = 0;
    // loading matrix 1
    r1 = c1 = 1;
    if (check_matrix_dim(&r1, &c1))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    int m1[r1][c1];
    if (ret == EXIT_SUCCESS && read_matrix(r1, c1, m1))
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
    r2 = c2 = 1;
    if (check_matrix_dim(&r2, &c2))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    int m2[r2][c2];
    if (ret == EXIT_SUCCESS && read_matrix(r2, c2, m2))
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;

    return ret;
}

void print_matrix(int rows, int cols, int matrix[rows][cols])
{
    fprintf(stderr, "%d %d\n", rows, cols);
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

bool sum(int r1, int c1, int m1[r1][c1], int r2, int c2, int m2[r2][c2], int r3,
         int c3, int m3[r3][c3], int sign)
{
    if (r1 == r2 && c1 == c2 && r1 == r3 && c1 == c3) {
        for (int r = 0; r < r1; ++r) {
            for (int c = 0; c < c1; ++c) {
                m3[r][c] = m1[r][c] + sign * m2[r][c];
            }
        }
        return true;
    } else
        return false;
}

bool multi(int r1, int c1, int m1[r1][c1], int r2, int c2, int m2[r2][c2],
           int m3[r1][c2], int sign)
{
    if (c1 == r2) {
        for (int r = 0; r < r1; ++r) {
            for (int c = 0; c < c2; ++c) {
                m3[r][c] = 0;
                for (int i = 0; i < r2; ++i) {
                    m3[r][c] += m1[r][i] * m2[i][c];
                }
            }
        }
        return true;
    } else
        return false;
}
