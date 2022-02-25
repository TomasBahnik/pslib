#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100;

enum { MANDATORY, OPTIONAL, ERROR };

int test_house_dim(int, int);
int test_fence_dim(int, int, int);

int print_house(int, int);
int print_fence(int, int, int);

int read_input(int *w, int *h, int *f_w);

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    int read = read_input(&w, &h, &f_w);
    if (read == MANDATORY) {
        printf("House dim is: %d x %d\n", w, h);
    } else if (read == OPTIONAL) {
        printf("House dim is: %d x %d + %d\n", w, h, f_w);
    } else {
        ret = ERROR_WRONG_INPUT;
    }
    return ret;
}

int read_input(int *w, int *h, int *f_w)
{
    int ret = ERROR;
    if (scanf("%d %d", w, h) == 2) {
        ret = MANDATORY;
    }
    if (ret == MANDATORY && *w == *h && scanf("%d", f_w) == 1) {
        ret = OPTIONAL;
    }
    return ret;
}

int print_house(int w, int h)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
    }
    return ret;
}

int print_fence(int w, int h, int f_w)
{
    int ret = test_house_dim(w, h);
    if (ret == 0) {
        ret = test_fence_dim(w, h, f_w);
    }
    if (ret == 0) {
    }
    return ret;
}

int test_house_dim(int w, int h)
{
    int ret = 0;
    return ret;
}

int test_fence_dim(int w, int h, int f_w)
{
    int ret = 0;
    if (f_w > 0 && f_w < h) {
        // OK
    } else {
        // CHYBA Error: Neplatna velikost plotu!
    }
    return ret;
}