//
// Created by pantom on 11.08.2022.
//

#include <stdio.h>

int main(void)
{
    int day, month, year;
    printf("Enter a date (mm/dd/yyyy) : \n");
    scanf("%d/%d/%d", &month, &day, &year);
    printf("You entered the date: %.4d%.2d%.2d\n", year, month, day);
    //printf("You entered the date: %.2d.%.2d.%.4d\n",day, month, year);
    return 0;
}
