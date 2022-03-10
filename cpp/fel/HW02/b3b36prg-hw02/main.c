#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define milion 1000000      // milion is 10 ** 6
#define primes_in_mil 78498 // count of prime numbers in milion

long int read_number(void);
int decompose(long int n, int primes[]);
void prime_numbers(int primes[]);
int print_output(int counter, int i, long int actual_num, long int n,
                 int primes[]);

// solution 1 // mandatory
// deviding input by smaller number than input number

// solution 2 // optional
// dividing by smaller numbers && algorithm end when dividend is smaller than
// divisor

// solution 3 // optional
// Sieve of Eratosthenes

int main(int argc, char *argv[])
{
    int primes[primes_in_mil];
    int ret = EXIT_SUCCESS;
    long int n;
    while ((n = read_number()) > 0) {
        printf("Prvociselny rozklad cisla %ld je:\n", n);
        prime_numbers(primes);
        decompose(n, primes);
    }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ERROR_INPUT;
    }
    return ret;
}

long int read_number(void)
{
    long int n = -1;
    if (scanf("%ld", &n) != 1) {
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
        }
    }
}

int decompose(long int n, int primes[])
{
    int counter = 0; // counting exponent
    long int actual_num = n;
    for (int i = 0; i < primes_in_mil; ++i) {
        counter = 0;
        // while cyclus for every i that is integer divisor for our
        // number
        while (actual_num % primes[i] == 0) {
            actual_num = actual_num / primes[i];
            counter += 1;
        }
        // condition true behind last printed number ---> doesn't print x at the
        // end of row
        if (actual_num == 1) {
            print_output(counter, i, actual_num, n, primes);
            printf("\n");
            return EXIT_SUCCESS;
        }
        print_output(counter, i, actual_num, n, primes);
    }
    return EXIT_SUCCESS;
}

int print_output(int counter, int i, long int actual_num, long int n,
                 int primes[])
{
    // condition true only if input number is 1
    if (n == 1) {
        printf("1");
        return EXIT_SUCCESS;
    }
    // condition true if input number has prime numbers only once
    if (counter == 1)
        printf("%d", primes[i]);
    // condition true if input number has multiple of same prime number
    if (counter > 1)
        printf("%d^%d", primes[i], counter);

    // condition true if while cyclus run at least once
    if (counter != 0 && actual_num != 1)
        printf(" x ");

    return EXIT_SUCCESS;
}
