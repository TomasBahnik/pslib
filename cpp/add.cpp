#include <iostream>
using namespace std;

int add(int x, int y)
{
	//add 2 numbers
	cout << "Running calculator ...\n";
	return (x+y);
}

int main()
{
	cout << "What is 867 + 5309?\n";
	cout << "The sum is " << add(867, 5309) << "\n\n";
	return 0;
}
