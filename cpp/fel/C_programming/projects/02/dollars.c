//
// Created by pantom on 04.08.2022.
//
#include <stdio.h>

int main(void)
{
    int x;
    printf("Enter amount in $: ");
    scanf("%d", &x);
    int divisor = 20;
    int count = 0;
    while (x > 1) {
        if (x < 5 && x > 1) {
            divisor = 1;
        }
        if (x >= divisor) {
            x = x - divisor;
            count += 1;
            if (x < divisor || x == 1) {
                printf("$ %d bills: %d\n", divisor, count);
            }
        } else {
            count = 0;
            divisor = divisor / 2;
        }
    }
    return 0;
}
