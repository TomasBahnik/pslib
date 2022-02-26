#include <stdio.h>

int main(void ) {
    int i, *pi;
    printf("uninitialized pointer value at %p is %d\n", pi, *pi);
    pi = &i;
    printf("initialized pointer value at %p is %d\n", pi, *pi);
    *pi = 123;
    printf("assigned pointer value at %p is %d\n", pi, *pi);
    return 0;
}