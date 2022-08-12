//
// Created by pantom on 12.08.2022.
//

#include <stdio.h>

int main(void) {
    int gsi, group, code, item, digit;
    printf("Enter ISBN: ");
    scanf("%d-%d-%d-%d-%d", &gsi, &group, &code, &item, &digit);
    printf("GSI prefix: %d\n", gsi);
    printf("Group identifier: %d\n", group);
    printf("Publisher code: %d\n", code);
    printf("Item number: %d\n", item);
    printf("Check digit: %d\n", digit);

    return 0;
}
