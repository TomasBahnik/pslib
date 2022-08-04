//
// Created by pantom on 28.07.2022.
//
#include <stdio.h>
#include <stdlib.h>

int main (void) {
    int r = 0;

    printf("Type a radius in metres: ");
    scanf("%d", &r);

    printf("Sphere of circle with radius %i metres is: ",r);
    printf("%.2f cubic metres\n",4.0/3.0 * 3.14 * r * r * r);
    return 0;
}
