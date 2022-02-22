#include <stdio.h>
#include <stdlib.h>
enum { ERROR_OK = EXIT_SUCCESS, ERROR_NO_INPUT = 100, ERROR_RANGE = 100 };

#define MAX_VALUE 100
#define MIN_VALUE -100

int main(int argc, char *argv[])
{
    int ret = ERROR_OK;
    int v;
    int c; // counter change comment iiii
    int sum;
    c = sum = 0;
    while (ret == ERROR_OK) {
        int r = scanf("%d", &v);
        if (r == 1) {
        } else if (r == EOF) {
            // end of input
        } else {
            ret = ERROR_NO_INPUT;
        }

        return ret;
    }
}