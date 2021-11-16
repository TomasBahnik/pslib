# Experimenty s radix sort

def num_digits(a):
  """ počet číslic v desítkovém zápisu čísla a """
  num=1
  while a>10:
    a//=10
    num+=1
  return num

def digit(a,n):
  """ n-tá číslice zprava čísla 'a', počítáno od nuly"""
  return a//(10**n) % 10


def radix_sort_integers(a):
  """ setřídí pole přirozených čísel s omezeným počtem číslic """
  max_digits=num_digits(max(a)) # max. počet číslic
  for i in range(max_digits):
    a=sort_by_digit(a,i)
  return a

def sort_by_digit(a,i):
  """ setřídí pole 'a' dle i-té číslice """  
  prihradka=[ [] for j in range(10) ]
  for x in a:
    c=digit(x,i) # číslice pro třídění
    prihradka[c]+=[x]
  r=[]
  for p in prihradka:
    r+=p
  return r  

import random
import sorting_experiments
import merge_sort_experiments
import quick_sort_experiments

def radix_sort_inplace(a):
  a[:]=radix_sort_integers(a)

def main():  
    a=[random.randrange(100) for i in range(10)]
    print(a)
    print(radix_sort_integers(a))

    sorting_experiments.test_sort(f=radix_sort_inplace)  

    sorting_experiments.time_sorting_algorithms(algs=[merge_sort_experiments.merge_sort,
                                                      quick_sort_experiments.quick_sort,radix_sort_integers,
                                                      sorting_experiments.python_sort],
                                                      prefix="time_with_radixsort",
                                                      ns=[1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000])

if __name__=="__main__":
  main()    
    
 
