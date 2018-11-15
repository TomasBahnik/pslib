#include <iostream>

int add(int x, int y)
{
	//add 2 numbers
	std::cout << "Running calculator ...\n";
	return (x+y);
}

int main()
{
	std::cout << "What is 867 + 5309?\n";
	std::cout << "The sum is " << add(867, 5309) << "\n\n";
	return 0;
}
