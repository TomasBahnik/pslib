class Complex:
    def __init__(self, real, imag):
        print(" TADY ")
        self.real = real
        self.imag = imag
        self.print()
    def print(self):
        print("metoda print", self.real, self.imag)


a = Complex(10, 10)
a.print()
# b = Complex(1, 5)
# b.imag = 2000
# print(a.real, a.imag)
# print(b.real, b.imag)


# class Complex:
#     def __init__(self, real, imag):
#         print(" TADY ")
#         self.real = real
#         self.imag = imag
#
#
# a = Complex(10, 10)
# b = Complex(1, 5)
# b.imag = 2000
# print(a.real, a.imag)
# print(b.real, b.imag)
