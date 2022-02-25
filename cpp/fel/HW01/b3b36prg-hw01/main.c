#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_WRONG_INPUT 100;

int main(int argc, char *argv[])
{
    int ret = 0;
    int w, h, f_w;
    _Bool fence = false;

    if (scanf("%d %d", &w, &h) == 2) {
        if (scanf("%d", &f_w) == 1) {
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
