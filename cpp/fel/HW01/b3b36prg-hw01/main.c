#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define NO_ERROR 0
#define ERROR_WRONG_INPUT 100
#define ERROR_HOUSE_DIM_OUT_OF_RANGE 101
#define ERROR_HOUSE_WITH_IS_NOT_ODD 102
#define ERROR_FENCE_WIDTH_INVALID 103
const int house_dim_min = 3;
const int house_dim_max = 69;

enum { MANDATORY, OPTIONAL }; //, ERROR_WRONG_INPUT = 100 };

int test_house_dim(int w, int h);
int test_fence_dim(int h, int f_w);

int print_roof(int, int);
int print_house(int, int);
int print_fence(int, int, int);

int read_input(int *w, int *h, int *f_w);

int main(int argc, char *argv[])
{
    int ret = NO_ERROR;
    int w, h, f_w;
    ret = read_input(&w, &h, &f_w);
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
    case ERROR_FENCE_WIDTH_INVALID:
        fprintf(stderr, "Error: Neplatna velikost plotu!\n");
        break;
    /*
     * All errors handled => only printing.
     * MANDATORY is value 0 same as NO_ERROR
     * OPTIONAL is value 1
     * It would be better to use some defined constants
     * But in previous cases 0 (NO_ERROR) and 1 are not checked so this the
     * only place where 0 and 1 can fall
     */
    case MANDATORY:
        print_roof(w, h);
        ret = print_house(w, h);
        break;
    case OPTIONAL:
        ret = print_fence(w, h, f_w);
        break;
    // Just for sure
    default:
        printf("Default case");
        break;
    }
    return ret;
}

/*
 * Validate input before plotting anything
 */
int read_input(int *w, int *h, int *f_w)
{
    int ret = ERROR_WRONG_INPUT;
    int test_dims_code = NO_ERROR;
    if (scanf("%i %i", w, h) == 2) {
        test_dims_code = test_house_dim(*w, *h);
        if (test_dims_code != NO_ERROR) {
            return test_dims_code;
        }
        // width and height are OK
        ret = MANDATORY;
    }
    //decides if read also fence width
    bool read_fence_width = ret == MANDATORY && *w == *h;
    if (read_fence_width) {
        bool fence_width_value_ok = scanf("%i", f_w) == 1;
        if (!fence_width_value_ok) {
            //wrong fence width return immediately
            return ERROR_WRONG_INPUT;
        }
        test_dims_code = test_fence_dim(*h,*f_w);
        if (test_dims_code != NO_ERROR) {
            return test_dims_code;
        }
        ret = OPTIONAL;
    }
    return ret;
}

/*
 * Only printing, no validity checks
 */
int print_roof(int w, int h)
{
    int roof_height = (w - 1) / 2; // height of roof
    for (int i = 0; i < roof_height; ++i) {
        for (int j = 0; j < roof_height + i + 1; ++j) {
            if ((j == roof_height + i) || ((j == roof_height - i)))
                printf("X");
            else
                printf(" ");
        }
        printf("\n");
    }
    return NO_ERROR;
}

/*
 * Only printing, no validity checks
 */
int print_house(int w, int h)
{
    // printf("House dim is: %d x %d\n", w, h);
    for (int i = 0; i < h; ++i) {
        for (int j = 0; j < w; ++j) {
            if ((i == 0) || (i == h - 1))
                printf("X");
            if ((j == 0) && (i >= 1) && (i < h - 1))
                printf("X");
            if ((j < w - 2) && (i >= 1) && (i < h - 1))
                printf(" ");
            if ((j == w - 1) && (i >= 1) && (i < h - 1))
                printf("X");
        }
        printf("\n");
    }
    return NO_ERROR;
}

/*
 * Only printing, no validity checks
 */
int print_fence(int w, int h, int f_w)
{
    printf("Print fence for house with dim: %d x %d + %d\n", w, h, f_w);
    return NO_ERROR;
}

int test_house_dim(int w, int h)
{
    int ret = NO_ERROR;
    int dim_ok = (house_dim_min <= w) && (w <= house_dim_max) &&
                 (house_dim_min <= h) && (h <= house_dim_max);
    if (!dim_ok) {
        ret = ERROR_HOUSE_DIM_OUT_OF_RANGE;
        // test on invalid dimension goes before test of width
        return ret;
    }
    if (w % 2 == 0) {
        ret = ERROR_HOUSE_WITH_IS_NOT_ODD;
        return ret;
    }
    return ret;
}

int test_fence_dim(int h, int f_w)
{
    if (f_w > 0 && f_w < h) {
        return NO_ERROR;
    } else {
        return ERROR_FENCE_WIDTH_INVALID;
    }
}
