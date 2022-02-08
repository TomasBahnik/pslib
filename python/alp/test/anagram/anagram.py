"""
Program hledama dvojice anagramu

UVOD
anagram = textovy retezec(string), ktery pouzitim vsech pismen z puvodniho retezce zmeni jejich poradi
napr. : debid card ---> bad credit


VSTUP: txt soubor jako prvni argument
        - na kazdem radku tohoto souboru je string, ktery muze obsahovat mala/velka pismena a mezery


VYSTUP: Seznam dvojic celych cisel (vzdy jedna dvojice na radku), nebo slovo ‘None’(pokud neobsahuje zadne angramy)
        vytistene na standardni vystup
        - dvojice cisle jsou indexy radku ve vstupnim souboru, ktere jsou anagramy
        - indexy jsou psany vzestupne dle druheho indexu (10 11, 10 12, 10 13, 11 12, 11 13 ...)

napr. :
    abc
    Abc
    a c b
    cA b
---> 0 2
     1 3
nebo
    tacts
    lemur
    bonny
    argue
    asttc
    ruelm
    onbyn
    gaeru
---> 0 4
     1 5
     2 6
     3 7

priklady anagramu :
 - ‘abc’, anagramem je napr.  ‘bca’, ‘cab’, ‘c a b’, ‘ a c b’ (mezery se neuvazuji)
 - ‘abc’ a ‘ a a b c ’ nejsou anagramy (nesouhlasi pocet pismen)
 - ‘Ac’ a ‘CA’ nejsou anagramy (case-sensitive)
 - ‘forty five’, priklad anagramu:  ‘over fifty’ nebo ‘overfifty’ nebo ‘fiftyover’
"""
import sys


def remove_spaces(s1):
    tmp = s1
    tmp = tmp.strip()
    tmp = tmp.replace(' ', '')
    return tmp


def is_anagram(s1, s2):
    return sorted(remove_spaces(s1)) == sorted(remove_spaces(s2))


def test(s1, s2):
    print("{} and {} are anagram {}".format(s1, s2, is_anagram(s1, s2)))


def all_tests():
    test('abc', 'a b c')
    test('abc', 'a c b')
    test('forty five', 'over fifty')
    test('forty five', 'fiftyover')
    test('Ac', 'CA')
    test('Ac', 'cA')


def load_input(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(line.strip())
        # print(pole)
    return pole


if __name__ == '__main__':
    load_input(sys.argv[1])
    # all_tests()
    sys.exit(0)
