//
// Created by pantom on 11.08.2022.
//

#include <stdio.h>

int main(void)
{
    int number, month, day, year;
    float price;
    printf("Enter item number: ");
    scanf("%d", &number);
    printf("Enter unit price: ");
    scanf("%f", &price);
    printf("Enter purchase date (mm/dd/yyyy) : \n");
    scanf("%d/%d/%d", &month, &day, &year);
    printf("Item\t Unit\t Purchase\n\t Price\t Date\n");
    printf("%d\t %.2f\t %.2d/%.2d/%.4d\n", number, price, month, day, year);

    return 0;
}
