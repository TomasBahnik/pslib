#include "erat_sieve.h"
#include <stdio.h>
int *e_s()
{
    int i, j;
    int number = MAX_NUM;
    static int primes[MAX_NUM + 1];

    // populating array with naturals numbers
    for (i = 2; i <= number; i++)
        primes[i] = i;
    i = 2;
    while ((i * i) <= number) {
        if (primes[i] != 0) {
            for (j = 2; j < number; j++) {
                if (primes[i] * j > number)
                    break;
                else
                    // Instead of deleting set to 0
                    primes[primes[i] * j] = 0;
            }
        }
        i++;
    }
    return primes;
}

int *prime_numbers_fce()
{
    static int primes[MAX_NUM] = {0};
    int j, i;
    int prime_count = 0;
    for (i = 2; i < MAX_NUM; ++i) {
        if (primes[i] == 0) {
            for (j = i; j < MAX_NUM; j += i) {
                primes[j] = 1;
            }
            primes[i] = 0; // set the prime index back to 0
            prime_count++;
        }
    }
    printf("for %i : number of primes = %i", MAX_NUM, prime_count);
    return primes;
}

int prime_numbers_dec(int n)
{
    int primes[MAX_NUM] = {0};
    int j, i;
    int prime_count = 0;
    int m = n;
    for (i = 2; i < MAX_NUM; ++i) {
        if (primes[i] == 0) {
            for (j = i; j < MAX_NUM; j += i) {
                primes[j] = 1;
            }
            primes[i] = 0; // set the prime index back to 0
            while (m % i == 0) {
                if (m == n) {
                    printf("%i=", n);
                }
                if (m / i == 1) {
                    printf("%i\n", i);
                    break;
                } else {
                    printf("%i*", i);
                    m = m - m / i;
                }
            }
            prime_count++;
        }
    }
    //    printf("for %i : number of primes = %i", MAX_NUM, prime_count);
    return 0;
}