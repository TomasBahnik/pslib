#include <stdio.h>

// input 1-20.3-4.0e3
int main() {
    int i, j;
    float x, y;
//    scanf("%d%d%f%f", &i, &j, &x, &y);
//    printf("%d\n", i);
//    printf("%d\n", j);
//    printf("%f\n", x);
//    printf("%f\n", y);

    printf(" d/d/==== \n");
    scanf("%d/%d", &i, &j);
    printf("%d\n", i);
    printf("%d\n", j);

    printf(" stdin ==== \n");
    // use inout.log
    fscanf(stdin, "%d/%d", &i, &j);
    printf("%d\n", i);
    printf("%d\n", j);
    return 0;
}