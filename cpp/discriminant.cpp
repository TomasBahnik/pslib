#include <iostream>
#include <math.h>       /* sqrt */

int main() {
    float a, b, c, result, Fi, sinus;
    a = 1;
    b = 5;
    c = 5;
    Fi = 3.14;
    sinus = sin(Fi);
    result = sqrt(b * b - 4 * a * c);
    printf("b^2 = %f, 4ac = %f, determinant = %f\n", b * b, 4 * a * c, result);
    printf("sinus %f = %f\n", Fi, sinus);
    return 0;
}
