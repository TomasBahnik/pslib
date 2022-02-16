#include <stdio.h>

void test_print_1();

void test_print() {
    printf("%6d,%4d", 86, 1040);
    printf("\n");
    printf("%12.5e", 3.14159265);
    printf("\r");
    printf("%.4f\n", 85.167);
}

int main() {
    test_print_1();
    test_print();
    return 0;
}

void test_print_1() {
    char c = 'a';
    int i = 1000, j;
    float x, y = 3.1415;

    printf("%c\n", c);
    printf("%i\n", c);
    printf("===\n");

    printf("%d\n", i);
    printf("%+5d\n", i);
    printf("%x\n", i);
    printf("===\n");

    printf("%f\n", y);
    printf("%10.3f\n", y);
    printf("\t%-g\n", y);
}
