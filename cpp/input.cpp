#include <iostream>
using namespace std;

int main ()
{
	int grade;
	cout << "Zadej cislo (1-100): ";
	cin >> grade;
	if (grade >= 70) 
		cout << "\nVic nez 70!\n";
	else
		cout << "\nMin nez 70!\n";
	return 0;	
}
