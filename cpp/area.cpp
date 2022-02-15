#include <iostream>

using namespace std;

int findArea(int length, int width);

int main() {
    int length;
    int width;
    int area;
    cout << "Zadej delku v m : ";
    cin >> length;
    cout << "Zadej sirku v m : ";
    cin >> width;
    area = findArea(length, width);
    cout << "\nPlocha je ";
    cout << area;
    cout << " metru ctverecnich \n\n";

    return 0;
}

// function definition
int findArea(int l, int w) {
    return l * w;
}
