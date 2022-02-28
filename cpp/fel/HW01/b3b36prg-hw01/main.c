#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100
#define ERROR_HOUSE_DIM_OUT_OF_RANGE 101
#define ERROR_HOUSE_WITH_IS_NOT_ODD 102
#define ERROR_FENCE_WIDTH_INVALID 103
const int house_dim_min = 3;
const int house_dim_max = 69;

enum { MANDATORY, OPTIONAL }; //, ERROR_WRONG_INPUT = 100 };

int test_house_dim(int w, int h);
int test_fence_dim(int h, int f_w);

int print_house(int, int);
int print_fence(int, int, int);

int read_input(int *w, int *h, int *f_w);

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    switch (ret = read_input(&w, &h, &f_w)) {
    case MANDATORY:
        ret = print_house(w, h);
        break;
    case OPTIONAL:
        ret = print_fence(w, h, f_w);
        break;
    }
    switch (ret) {
    case ERROR_WRONG_INPUT:
        fprintf(stderr,
                "Error: Chybny vstup!\n"); // tiskne pokud vstup neni cislo
        break;
    case ERROR_HOUSE_DIM_OUT_OF_RANGE:
        fprintf(stderr, "Error: Vstup mimo interval!\n");
        break;

    case ERROR_HOUSE_WITH_IS_NOT_ODD:
        fprintf(stderr, "Error: Sirka neni liche cislo!\n");
        break;
    }
    return ret;
}

int read_input(int *w, int *h, int *f_w)
{
    int ret = ERROR_WRONG_INPUT;
    if (scanf("%d %d", w, h) == 2) {
        ret = MANDATORY;
    }
    if (ret == MANDATORY && *w == *h &&
        scanf("%d", f_w) == 1) { // overi jestli je 3 vstup cele cislo
        ret = OPTIONAL;
    }
    return ret;
}

int print_house(int w, int h)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
        printf("House dim is: %d x %d\n", w, h);
    }
    return ret;
}

int print_fence(int w, int h, int f_w)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
        ret = test_fence_dim(h, f_w);
    }
    if (ret == 0) { // all test passed
        printf("House dim is: %d x %d + %d\n", w, h, f_w);
    }
    return ret;
}

int test_house_dim(int w, int h)
{
    int ret = 0;
    int dim_ok = (house_dim_min <= w) && (w <= house_dim_max) &&
                 (house_dim_min <= h) && (h <= house_dim_max);
    if (!dim_ok) {
        ret = ERROR_HOUSE_DIM_OUT_OF_RANGE;
    }
    if (w % 2 == 0) {
        ret = ERROR_HOUSE_WITH_IS_NOT_ODD;
    }
    return ret;
}

int test_fence_dim(int h, int f_w)
{
    int ret = 0;
    if (f_w > 0 && f_w < h) {
        // OK
    } else {
        printf("ERROR_FENCE_WIDTH_INVALID\n");
        ret = ERROR_FENCE_WIDTH_INVALID;
    }
    return ret;
}