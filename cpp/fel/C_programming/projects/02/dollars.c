//
// Created by pantom on 04.08.2022.
//
#include <stdio.h>

int main(void) {
    int x;
    printf("Enter amount in $: ");
    scanf("%d", &x);
    int divisor = 20;
    int count = 0;
    while (x > 0) {
        if (x < 5){
            divisor = 1;
        };
        if (x % divisor == 0) {
            count += 1;
            x = x - divisor;
            printf("$ %d bills: %d\n", divisor, count);
        } else {
            printf("$ %d bills: %d\n", divisor, count);
            count = 0;
            divisor = divisor / 2;
        }

    };

    return 0;
}
