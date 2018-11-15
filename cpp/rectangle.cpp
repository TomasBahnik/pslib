#include <iostream>

int main()
{
   // set up width and length
   unsigned short width = 26, length;
   length = 40;
   
   unsigned short area = width * length;
   
   std::cout << "Width  : " << width << "\n";
   std::cout << "Length : " << length << "\n";
   std::cout << "Area   : " << area << "\n";
   
   return 0;
}
