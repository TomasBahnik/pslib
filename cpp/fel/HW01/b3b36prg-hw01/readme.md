### Tests
Adresar `test` obsahuje testovaci data a testovaci script. Po spusteni vypise 
pouzita data, exit code, std error

Priklad

```shell
2022-02-28T21:43:54+0100 : compiling clang ../main.c -o main
2022-02-28T21:43:54+0100 : running 12 tests
------------------------------             
test_data    exit_code  error              
------------------------------             
[9 9 11]     103        Error: Neplatna velikost plotu!
[5 2]        101        Error: Vstup mimo interval!    
[5 234 156]  101        Error: Vstup mimo interval!    
[6 12]       102        Error: Sirka neni liche cislo! 
[12 12 10]   102        Error: Sirka neni liche cislo! 
[23 a]       100        Error: Chybny vstup!           
[13 13 c]    0                                         
[13 dgdg]    100        Error: Chybny vstup!           
[13 13.456]  0
[xyz]        100        Error: Chybny vstup!
[3 69 11]    0
[13 13 11]   0

```


