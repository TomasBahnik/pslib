#include <iostream>
#include <math.h>       /* sqrt */

int main ()
{
	float a,b,c,result;
	a=2;
	b=78;
	c=8;
	result = sqrt (b*b - 4*a*c);
	printf ("b^2 = %f, 4ac = %f, determinant = %f\n", b*b, 4*a*c, result);
	return 0;
}
