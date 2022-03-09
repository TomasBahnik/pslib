#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define milion 1000000      // milion is 10 ** 6
#define primes_in_mil 78498 // count of prime numbers in milion

// solution 1 // mandatory
// deviding input by smaller number than input number

int read_number(void);
void decompose(int n);
void prime_numbers(int primes[]);

// solution 2 // optional
// dividing by smaller numbers && algorithm end when dividend is smaller than
// divisor

// solution 3 // optional
// Sieve of Eratosthenes

int main(int argc, char *argv[])
{
    int primes[primes_in_mil];
    int ret = EXIT_SUCCESS;
    int n;
    // while ((n = read_number()) > 0) {
    //     printf("Prvociselny rozklad cisla %d je:\n", n);
    //     decompose(n);
    // }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ERROR_INPUT;
    }
    prime_numbers(primes);
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

void prime_numbers(int primes[])
{
    int empty[milion] = {0};
    int counter = 0;
    for (int i = 2; i < milion; ++i) {
        if (empty[i] == 0) {
            for (int j = i; j < milion; j += i) {
                empty[j] = 1;
            }
            primes[counter] = i;
            counter += 1;
            // printf("%d\n", i);
        }
    }
    printf("%d\n", primes[4]); // only test for me
}

void decompose(int n)
{
    // int actual_num = n;
    // for (int i = 0; i < primes_in_mil; ++i) {
    //     if (actual_num % i = 0) {
    //         actual_num = actual_num / i;
    //     }
    // }
    // printf("%d\n", n);
}
