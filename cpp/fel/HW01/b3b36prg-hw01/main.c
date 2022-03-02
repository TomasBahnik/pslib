#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100
#define ERROR_HOUSE_DIM_OUT_OF_RANGE 101
#define ERROR_HOUSE_WITH_IS_NOT_ODD 102
#define ERROR_FENCE_WIDTH_INVALID 103
const int house_dim_min = 3;
const int house_dim_max = 69;

enum { MANDATORY, OPTIONAL };

int test_house_dim(int w, int h);
int test_fence_dim(int h, int f_w);

int print_roof(int, int);
int print_house(int, int);
int print_fence(int, int, int);
void fill_house(int, int);

int read_input(int *w, int *h, int *f_w);

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    switch (ret = read_input(&w, &h, &f_w)) {
    case MANDATORY: // occurs if input has 2 numbers
        ret = print_roof(w, h);
        ret = print_house(w, h);
        break;
    case OPTIONAL: // occurs if input has 3 numbers
        ret = print_fence(w, h, f_w);
        ret = print_roof(w, h);
        ret = print_house(w, h);
        // ret = fill_house(w, h);
        break;
    } // end switch
    switch (ret) {
    case ERROR_WRONG_INPUT:
        fprintf(stderr, "Error: Chybny vstup!\n");
        // prints if the input is not a number
        break;

    case ERROR_HOUSE_DIM_OUT_OF_RANGE:
        fprintf(stderr, "Error: Vstup mimo interval!\n");
        // print if input is out of range
        break;

    case ERROR_HOUSE_WITH_IS_NOT_ODD:
        fprintf(stderr, "Error: Sirka neni liche cislo!\n");
        // print if width is not odd number
        break;

    case ERROR_FENCE_WIDTH_INVALID:
        fprintf(stderr, "Error: Neplatna velikost plotu!\n");
        // print if fence width is not smaller then house width
        break;
    } // end switch
    return ret;
}

int read_input(int *w, int *h, int *f_w)
{
    int ret = ERROR_WRONG_INPUT;
    if (scanf("%i %i", w, h) == 2) {
        ret = MANDATORY;
    }
    if (ret == MANDATORY && *w == *h &&
        scanf("%i", f_w) == 1) { // verify if third input is an integer
        ret = OPTIONAL;
    }
    return ret;
}

int print_roof(int w, int h)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
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
    }
    return 1;
}

int print_house(int w, int h)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
        // printf("House dim is: %d x %d\n", w, h);
        for (int i = 0; i < h; ++i) {
            for (int j = 0; j < w; ++j) {
                if ((i == 0) || (i == h - 1))
                    printf("X");
                if (((j == 0) || (j == w - 1)) && (i >= 1) && (i < h - 1))
                    printf("X");
                fill_house(w, h);
                // if ((j < w - 2) && (i >= 1) && (i < h - 1))
                //    printf(" ");
            }
            printf("\n");
        }
    }
    return ret;
}

void fill_house(int w, int h)
{
    int j;
    int i;

    if (test_fence_dim(w, h == true)) {
        if ((j < w - 2) && (i >= 1) && (i < h - 1))
            printf("o");
    } else {
        if ((j < w - 2) && (i >= 1) && (i < h - 1))
            printf(" ");
    }
}

int print_fence(int w, int h, int f_w)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
        ret = test_fence_dim(h, f_w);
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
        ret = ERROR_FENCE_WIDTH_INVALID;
    }
    return ret;
}