#include "erat_sieve.h"
#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define milion 1000000 // milion is 10 ** 6
int array[milion] = {0};
int *primes;
// solution 1 // mandatory
// deviding input by smaller number than input number

long read_number(void);
void decompose(long n);
void prime_numbers();

// solution 2 // optional
// dividing by smaller numbers && algorithm end when dividend is smaller than
// divisor

// solution 3 // optional
// Sieve of Eratosthenes

int main(int argc, char *argv[])
{
    int ret = EXIT_SUCCESS;
    long n;
    while ((n = read_number()) > 0) {
        decompose(n);
    }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup! %ld\n", n);
        return ERROR_INPUT;
    }
    return ret;
}

long read_number(void)
{
    long n = -1;
    if (scanf("%ld", &n) != 1) {
        n = -1;
    }
    return n;
}

void prime_numbers()
{
    int cnt = 0;
    for (int i = 2; i < milion; ++i) {
        if (array[i] == 0) {
            for (int j = i; j < milion; j += i) {
                array[j] = 1;
            }
            printf("prime[%i] = %d\n", cnt, i);
            cnt++;
        }
    }
    printf("\nprimes count = %i for %i.", cnt, milion);
}

void decompose(long n)
{
    printf("Prvociselny rozklad cisla %ld je:\n", n);
    prime_numbers_dec(n);
}
