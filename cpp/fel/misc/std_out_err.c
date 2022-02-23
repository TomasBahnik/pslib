#include <stdio.h>

int main() {
    int i = 1000;
    fprintf(stdout, "Standardní výstup xxx: %d\n", i);
    fprintf(stderr, "Error výstup: %d\n", i);
}