### Tests
Adresar `data` obsahuje testovaci data (in, out, err) a testovaci script. Po spusteni vypise 
pouzita data, exit code, std error

Priklad

```shell
2022-03-02T14:04:26+0100 : compiling with 'clang -pedantic -Wall -Werror -std=c99 ../main.c -o main'
2022-03-02T14:04:26+0100 : running 7 tests
------------------------------
test_data       exit_code  error
------------------------------
[7 4]           0          

   X
  X X
 X   X
XXXXXXX
X     X
X     X
XXXXXXX

[x 16]          100        Error: Chybny vstup!
[-4 16]         101        Error: Vstup mimo interval!
[8 21]          102        Error: Sirka neni liche cislo!
[9 9 6]         0

Print fence for house with dim: 9 x 9 + 6

[5 5 x]         100        Error: Chybny vstup!
[5 5 10]        103        Error: Neplatna velikost plotu!
```

