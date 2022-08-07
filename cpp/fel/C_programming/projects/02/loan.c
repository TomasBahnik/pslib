//
// Created by pantom on 06.08.2022.
//

#include <stdio.h>

int main(void) {
    float loan = 0;
    float rate = 0;
    float payment = 0;
    printf("Enter amount of loan: \n");
    scanf("%f", &loan);
    printf("Enter interest rate: \n");
    scanf("%f", &rate);
    printf("Enter monthly payment: \n");
    scanf("%f", &payment);
    int count = 0;
    char first[] = "first";
    char second[] = "second";
    char third[] = "third";
    while (count < 3) {
        float perc = ((loan/100) * rate) / 12;
        float res = loan - payment + perc;
        loan = res;
        count += 1;
        if (count == 1)
            printf("Balance remaining after %s payment: %.2f\n",first, res);
        if (count == 2)
            printf("Balance remaining after %s payment: %.2f\n",second, res);
        if (count == 3)
            printf("Balance remaining after %s payment: %.2f\n",third, res);
    }

    return 0;
}
