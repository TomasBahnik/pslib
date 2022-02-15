//
// Created by tomas.bahnik on 2/15/2022.
//

#include <iostream>
#include <sstream>

using namespace std;

std::string get_compiler_info() {
    std::stringstream ret_val;
#if defined(__clang__)
    ret_val <<"clang" << __clang_major__;
#elif defined(__GNUC__)
    ret_val << "gcc" << __GNUC__;
#endif
    return ret_val.str();
}

int findArea(int length, int width);

int test() {
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
    return area;
}

// function definition
int findArea(int l, int w) {
    return l * w;
}


int main() {
//    cout << get_compiler_info() << '\n';
    test();
}