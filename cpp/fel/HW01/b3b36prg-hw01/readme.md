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
Data s **exit_code=0** by mela vykresilt domecek a data s **exit_code != 0** by mela
vypsat pouze error

Priklad (chybny)

[ERROR_HOUSE_DIM_OUT_OF_RANGE](tests/ERROR_HOUSE_DIM_OUT_OF_RANGE.txt)

```shell
./main < ERROR_HOUSE_DIM_OUT_OF_RANGE.txt 
  X
 X X
Error: Vstup mimo interval!
```
```shell
./main < NO_ERROR_2.txt 
House dim is: 13 x 13 + 11
```


