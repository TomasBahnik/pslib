//
// Created by pantom on 01.08.2022.
//

#include <stdio.h>
int main(void) {
    float x;
    printf("Enter value of polynom: ");
    scanf("%f", &x);
    printf("value of x is: %.2f\n", x);
    float poly = ((((3 * x + 2) * x - 5) * x - 1) * x + 7) * x - 6;
    printf("summary od polynom is: %.2f\n",poly);
    return 0;
}
