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

"""