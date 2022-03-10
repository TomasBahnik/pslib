# Tests

* test data are in `HW02/b3b36prg-hw02/data` dir
* functions are in module `erat_sieve.c`

```shell
(base) toba@TBAHNIK:~/git/pslib/cpp/fel/HW02/b3b36prg-hw02/data$ ./test_all.sh 
2022-03-10T13:32:27+0100 : remove file 'b3b36prg-hw02'
2022-03-10T13:32:27+0100 : compiling with 'clang -pedantic -Wall -Werror -std=c99 -O3 -lm ../main.c -o b3b36prg-hw02'
2022-03-10T13:32:27+0100 : running 5 tests
-------------------------------
exit_code  status std error
-------------------------------
Test start : 1646915547.675028300 sec
0          PASS 
100        PASS  Error: Chybny vstup!
100        PASS  Error: Chybny vstup!
0          PASS 
0          PASS 
Test end : 1646915547.947157700 sec
```