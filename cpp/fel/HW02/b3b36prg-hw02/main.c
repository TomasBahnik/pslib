#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define MAX_NUM 1000000

long read_number(void);
void decompose(long n);

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
        printf("Prvociselny rozklad cisla %ld je:\n", n);
        decompose(n);
    }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup!\n");
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

void decompose(long n)
{
    if (n == 1) {
        printf("%li\n", n);
        return;
    }
    int primes[MAX_NUM] = {0};
    int j, i;
    long m = n;
    for (i = 2; i < MAX_NUM; ++i) {
        int exp = 0;
        if (primes[i] == 0) {
            for (j = i; j < MAX_NUM; j += i) {
                primes[j] = 1;
            }
            primes[i] = 0; // set the prime index back to 0
            while (m % i == 0) {
                exp++;
                if (m / i == 1) {
                    exp > 1 ? printf("%i^%i\n", i, exp) : printf("%i\n", i);
                    break;
                } else {
                    m = m / i;
                    if (m % i != 0) {
                        exp > 1 ? printf("%i^%i x ", i, exp)
                                : printf("%i x ", i);
                    }
                }
            }
        }
    }
}
