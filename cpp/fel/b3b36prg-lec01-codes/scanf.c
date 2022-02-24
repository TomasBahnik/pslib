#include <stdio.h>
#include <stdlib.h>

void read_agrs(int count, char **args);

int main(int argc, char **argv)
{
    read_agrs(argc, argv);
    int i;
    double d;

    int r = printf("Enter int value: ");
    r = scanf("%i", &i); /* operator & return address of the variable i */
    if (r == 1) {
        printf("Enter a double value: ");
    }
    if (scanf("%lf", &d) == 1) {
        printf("You entered %02i and %0.1f\n", i, d);
    }
    return 0; // return value of main() -- zero is exit success
}

void read_agrs(int count, char **args)
{
    int first;
    double second;
    char *eptr;
    switch (count) {
    case 1:
        printf("no agrs\n");
        printf("first %i, second %f\n", first, second);
        break;
    case 2:
        printf("1 arg\n");
        first = atoi(args[1]);
        printf("first %i, second %f\n", first, second);
        break;
    case 3:
        printf("2 args\n");
        first = atoi(args[1]);
        second = strtod(args[2], &eptr);
        printf("first %i, second %f\n", first, second);
        break;
    default:
        break;
    }
}
