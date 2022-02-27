#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100
#define ERROR_HOUSE_DIM_OUT_OF_RANGE 101
#define ERROR_HOUSE_WITH_IS_NOT_ODD 102
#define ERROR_FENCE_WIDTH_INVALID 103
#define ERROR_NONE_OF_THE_SWITCH_CASES 104
const int house_dim_min = 3;
const int house_dim_max = 69;

enum { MANDATORY, OPTIONAL, ERROR };

int test_house_dim(int w, int h);
int test_fence_dim(int h, int f_w);

int print_house(int, int);
int print_fence(int, int, int);

int read_input(int *w, int *h, int *f_w);
int assign_ret_val(char *message, int value);

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    ret = read_input(&w, &h, &f_w);
    switch (ret) {
    case ERROR_WRONG_INPUT:
        ret = assign_ret_val("ERROR_WRONG_INPUT",ERROR_WRONG_INPUT);
        break;
    case MANDATORY:
        ret = print_house(h, w);
        break;
    case OPTIONAL:
        ret = print_fence(h, w, f_w);
        break;
    default:
        ret = assign_ret_val("ERROR_NONE_OF_THE_SWITCH_CASES",ERROR_NONE_OF_THE_SWITCH_CASES);
        break;
    }
    return ret;
}

int read_input(int *w, int *h, int *f_w)
{
    int ret = ERROR;
    if (scanf("%d %d", w, h) == 2) {
        ret = MANDATORY;
    }
    if (ret == MANDATORY && *w == *h) {
        if (scanf("%d", f_w) == 1) { // overi jestli je 3 vstup cele cislo
            ret = OPTIONAL;
        } else {
            ret = ERROR_WRONG_INPUT;
        }
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
        ret = assign_ret_val("ERROR_HOUSE_DIM_OUT_OF_RANGE",ERROR_HOUSE_DIM_OUT_OF_RANGE);
        return ret;
    }
    if (w % 2 == 0) {
        ret = assign_ret_val("ERROR_HOUSE_WITH_IS_NOT_ODD",ERROR_HOUSE_WITH_IS_NOT_ODD);
        return ret;
    }
    return ret;
}

int test_fence_dim(int h, int f_w)
{
    int ret = 0;
    if (f_w > 0 && f_w < h) {
        // OK
    } else {
        ret = assign_ret_val("ERROR_FENCE_WIDTH_INVALID",ERROR_FENCE_WIDTH_INVALID);
    }
    return ret;
}

int assign_ret_val(char *message, int value)
{
    printf("%s\n", message);
    return value;
}
