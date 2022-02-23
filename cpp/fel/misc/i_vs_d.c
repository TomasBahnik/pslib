// C program to demonstrate the difference
// between %i and %d specifier
#include <stdio.h>

int main()
{
    int a, b, c;

    printf("Enter value of a in decimal format:");
    scanf("%d", &a);

    printf("Enter value of b in octal format: ");
    scanf("%i", &b);

    printf("Enter value of c in hexadecimal format: ");
    scanf("%i", &c);

    printf("a = %i, b = %i, c = %i\n", a, b, c);

    return 0;
}