#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100;
#define ERROR_HOUSE_DIM_OUT_OF_RANGE 101;
#define ERROR_HOUSE_WITH_IS_NOT_ODD 102;
#define ERROR_FENCE_WIDTH_INVALID 103;
const int house_dim_min = 3;
const int house_dim_max = 69;

int test_house_dim(int w, int h);
int test_fence_dim(int h, int f_w);

int Print_house(int, int);
int Print_fence(int, int, int);

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    _Bool fence = false;

    if (scanf("%d %d", &w, &h) == 2) {
        test_house_dim(w, h);
        if (w == h && scanf("%d", &f_w) == 1) {
            test_fence_dim(h, f_w);
            fence = true;
        }
    } else {
        ret = ERROR_WRONG_INPUT;
    }

    if (!fence) {
        printf("House dim is: %d x %d\n", w, h);
    } else {
        printf("House dim is: %d x %d + %d\n", w, h, f_w);
    }

    return ret;
}

int Print_house(int w, int h)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
    }
    return ret;
}

int Print_fence(int w, int h, int f_w)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
        ret = test_fence_dim(h, f_w);
    }
    if (ret == 0) {
    }
    return ret;
}

int test_house_dim(int w, int h)
{
    int ret = 0;
    int dim_ok = (house_dim_min <= w <= house_dim_max) &&
                 (house_dim_min <= h <= house_dim_max);
    if (!dim_ok) {
        ret = ERROR_HOUSE_DIM_OUT_OF_RANGE
    }
    if (w % 2 == 0) {
        ret = ERROR_HOUSE_WITH_IS_NOT_ODD
    }
    return ret;
}

int test_fence_dim(int h, int f_w)
{
    int ret = 0;
    if (f_w > 0 && f_w < h) {
        // OK
    } else {
        ret = ERROR_FENCE_WIDTH_INVALID
    }
    return ret;
}