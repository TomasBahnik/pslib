#include "erat_sieve.h"
#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define milion 1000000 // milion is 10 ** 6
int array[milion] = {0};
int *primes;
// solution 1 // mandatory
// deviding input by smaller number than input number

int read_number(void);
void decompose(int n);
void prime_numbers();

// solution 2 // optional
// dividing by smaller numbers && algorithm end when dividend is smaller than
// divisor

// solution 3 // optional
// Sieve of Eratosthenes

int main(int argc, char *argv[])
{
    int ret = EXIT_SUCCESS;
    int n, i, j;
    // while ((n = read_number()) > 0) {
    //     printf("Prvociselny rozklad cisla %d je:\n", n);
    //     decompose(n);
    // }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ERROR_INPUT;
    }
    // prime_numbers();
    // function from module erat_sieve.c
    // MAX_NUM is set in header file erat_sieve.h
    primes = prime_numbers_fce();
    // count the nuber of primes in order to create array with primes only
    int prime_count = 0;
    for (i = 2; i <= MAX_NUM; ++i) {
        // If number is not 0 then it is prime
        if (primes[i] == 0)
            prime_count++;
    }
    // create array with primes only
    int primes_only[prime_count];
    j = 0;
    for (i = 2; i < MAX_NUM; ++i) {
        if (primes[i] == 0) {
            primes_only[j] = primes[i];
            j++;
        }
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
// void decompose(int n)
// {
//     int array[milion] = {0};
//     array[2] = 1;
//     for (int i = 2; i < milion; ++i) {
//         if (array[i] == 0) {
//             for (int j = 2; j < milion; ++j) {
//                 if (j % i == 0) {
//                     array[j] = 1;
//                 }
//             }
//         }
//         if (array[i] == 0)
//             printf("%d\n", i);
//     }
// }
