#include <stdio.h>
#include <stdlib.h>

// solution 1 // mandatory
// deviding input by smaller number than input number
int read_number(void);
int decompose(int n);

// solution 2 // optional
// dividing by smaller numbers && algorithm end when dividend is smaller than
// divisor

// solution 3 // optional
// Sieve of Eratosthenes
enum { ERROR_INPUT = 100 };

int main(int argc, char *argv[])
{
    int ret = EXIT_SUCCESS;
    int n;
    while ((n = read_number()) > 0) {
        printf("Prvociselny rozklad cisla %d je:\n", n);
        decompose(n);
    }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ERROR_INPUT;
    }
    return ret;
}

int read_number(void)
{
    int n = -1;
    if (scanf("%d", &n) != 1) {
        n = -1;
    }
    return n;
}

int decompose(int n)
{
    printf("rozklad\n");
    return 0;
}
