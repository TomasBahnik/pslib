#include <iostream>

int main()
{
	std::cout << "The size of an integer:\t\t";
	std::cout << sizeof(int) << " bytes\n";
	
	std::cout << "The size of a short integer:\t";
	std::cout << sizeof(short) << " bytes\n";
	
	std::cout << "The size of a long long int:\t";
	std::cout << sizeof(long long int) << " bytes\n";
	return 0;
}
