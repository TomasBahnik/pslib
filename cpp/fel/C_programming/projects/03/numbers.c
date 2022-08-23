//
// Created by pantom on 17.08.2022.
//

#include <stdio.h>

int main(void){
    int a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p;
    int col_sum, row_sum, dig_sum;
    scanf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d",&a,&b,&c,&d,&e,&f,&g,&h,&i,&j,&k,&l,&m,&n,&o,&p);
    printf("\n");
    printf("%3d%3d%3d%3d\n%3d%3d%3d%3d\n%3d%3d%3d%3d\n%3d%3d%3d%3d\n",a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p);
    printf("Row sums: %3d%3d%3d%3d\n", a+b+c+d, e+f+g+h, i+j+k+l, m+n+o+p);
    printf("Column sums: %3d%3d%3d%3d\n", a+e+i+m, b+f+j+n, c+g+k+o, d+h+l+p);
    printf("Diagonal sums: %3d%3d\n", a+f+k+p, d+g+j+m);
    return 0;
}
// input: 16 3 2 13 5 10 11 8 9 6 7 12 4 15 14 1
