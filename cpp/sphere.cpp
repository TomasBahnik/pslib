#include <iostream>
#include <math.h>
using namespace std;

double findArea(double radius);
double findVolume(double radius);

int main ()
{
	double radius;
	double area;
	double volume;
	cout << "Zadej polomer v m : ";
	cin >> radius;
	area = findArea(radius);
	volume = findVolume(radius);
	cout << "\nPlocha koule o polomeru ";
	cout << radius;
	cout << " m je ";
	cout << area;
	cout << " metru ctverecnich.\n";
	
	cout << "Objem koule o polomeru ";
	cout << radius;
	cout << " m je ";
	cout << volume;
	cout << " metru krychlovych.\n\n";

	cout << "\nPouzivana hodnota pi = ";
	cout << M_PI;

	return 0;	
}

// function definition
double findArea(double r) {
	return 4.0 * M_PI * pow(r,2);
}

double findVolume(double r) {
	return 4.0/3.0 * M_PI * pow(r,3);
}
