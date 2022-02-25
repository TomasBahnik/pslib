#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100;

int Test_house_dim(int, int);
int Test_fence_dim(int, int, int);

int Print_house(int, int);
int Print_fence(int, int, int);

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    _Bool fence = false;

    if (scanf("%d %d", &w, &h) == 2) {
        if (w == h && scanf("%d", &f_w) == 1) {
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
    int ret = Test_house_dim(w, h);
    if (ret == 0) {
    }
    return ret;
}

int Print_fence(int w, int h, int fw)
{
    int ret = Test_house_dim(w, h);
    if (ret == 0) {
        ret = Test_fence_dim(w, h, fw);
    }
    if (ret == 0) {
    }
    return ret;
}

int Test_house_dim(int w, int h)
{
    int ret = 0;
    return ret;
}

int Test_fence_dim(int w, int h, int fw)
{
    int ret = 0;
    if (fw > 0 && fw < h) {
        // OK
    } else {
        // CHYBA Error: Neplatna velikost plotu!
    }
    return ret;
}