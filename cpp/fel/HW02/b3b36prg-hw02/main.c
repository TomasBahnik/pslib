#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define milion 1000000 // milion is 10 ** 6
int array[milion] = {0};
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
    int n;
    // while ((n = read_number()) > 0) {
    //     printf("Prvociselny rozklad cisla %d je:\n", n);
    //     decompose(n);
    // }
    if (n < 0) {
        fprintf(stderr, "Error: Chybny vstup!\n");
        return ERROR_INPUT;
    }
    prime_numbers();
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
    for (int i = 2; i < milion; ++i) {
        if (array[i] == 0) {
            for (int j = i; j < milion; j += i) {
                array[j] = 1;
            }
            printf("%d\n", i);
        }
    }
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
