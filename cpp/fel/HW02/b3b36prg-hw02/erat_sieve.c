#include <stdio.h>
#include "erat_sieve.h"
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
