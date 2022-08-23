#include <stdio.h>

void books(void)
{
    int gsi, group, code, item, digit;
    printf("Enter ISBN: ");
    scanf("%d-%d-%d-%d-%d", &gsi, &group, &code, &item, &digit);
    printf("GSI prefix: %d\n", gsi);
    printf("Group identifier: %d\n", group);
    printf("Publisher code: %d\n", code);
    printf("Item number: %d\n", item);
    printf("Check digit: %d\n", digit);
}

void dates(void)
{
    int day, month, year;
    printf("Enter a date (mm/dd/yyyy) : \n");
    scanf("%d/%d/%d", &month, &day, &year);
    printf("You entered the date: %.4d%.2d%.2d\n", year, month, day);
    // printf("You entered the date: %.2d.%.2d.%.4d\n",day, month, year);
}

void products(void)
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
}
