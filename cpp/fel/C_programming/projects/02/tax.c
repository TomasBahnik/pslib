//
// Created by pantom on 01.08.2022.
//
#include <stdio.h>
int main(void) {
    float money;
    scanf("%f", &money);
    float tax = (money/100) * 5;
    printf("Entered amount is: %.2f $\n", money);
    printf("With tax added: %.2f $\n", money + tax);
    return 0;
}
