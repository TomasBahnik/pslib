#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

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
    if (check_matrix_dim(&row1, &col1)) // check first metrix dimension
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    int m1[row1][col1];
    if (ret == EXIT_SUCCESS &&
        read_matrix(row1, col1, m1)) // check first metrix values
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;

    if (ret == ERROR_INPUT) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ret;
    }
    // loading char between matrix 1 and 2
    char op[2];
    if (scanf("%1s", op) == 1) // check symbol
        ret = EXIT_SUCCESS;

    // loading matrix 2
    int row2, col2;
    row2 = col2 = 1;
    if (check_matrix_dim(&row2, &col2)) // check second metrix dimension
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;
    int m2[row2][col2];
    if (ret == EXIT_SUCCESS &&
        read_matrix(row2, col2, m2)) // check second metrix values
        ret = EXIT_SUCCESS;
    else
        ret = ERROR_INPUT;

    if (ret == ERROR_INPUT) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ret;
    }

    int sign = 1;
    int sum_res[row1][col1]; // sum resolution
    int mul_res[row1][col2]; // multiply resolution
    switch (op[0]) {
    case '-': // inversion to sum function
        sign = -1;
    case '+': // sum function
        if (sum(row1, col1, m1, row2, col2, m2, row1, col1, sum_res,
                sign) == true) // condition check rules for sum matrix
            print_matrix(row1, col1, sum_res);
        else
            ret = ERROR_INPUT;
        break;
    case '*': // multiplication function
        if (multi(row1, col1, m1, row2, col2, m2, mul_res, sign) ==
            true) // condition check rules for multiply matrix
            print_matrix(row1, col2, mul_res);
        else
            ret = ERROR_INPUT;
        break;
    default:
        ret = ERROR_INPUT;
        break;
    } // end of switch
    return ret;
}

void print_matrix(int rows, int cols, int matrix[rows][cols])
{
    printf("%d %d\n", rows, cols);
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            printf("%d", matrix[r][c]);
            if (c != cols - 1) // dont print last space
                printf(" ");
        }
        printf("\n");
    }
}

bool check_matrix_dim(int *r, int *c) { return scanf("%d %d", r, c) == 2; }

bool read_matrix(int rows, int cols, int matrix[rows][cols])
{
    bool ret = false;
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
    } else {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return false;
    }
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
    } else {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return false;
    }
}
