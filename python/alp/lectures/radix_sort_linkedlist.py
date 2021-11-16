# Implementace radix sort (příhrádkového třídění) pomocí spojových seznamů
#
# Jan Kybic, 2016


from linkedlistqueue import ListQueue,array_to_queue

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


def radix_sort_array_integers(a):
  """ setřídí pole přirozených čísel s omezeným počtem číslic """
  q=radix_sort_queue_integers(array_to_queue(a))
  return q.to_array()

def radix_sort_queue_integers(q):
  """ setřídí frontu ListQueue přirozených čísel s max_digits číslicemi """
  max_digits=num_digits(q.reduce(max,0))
  for i in range(max_digits):
    q=sort_queue_by_digit(q,i)
  return q
    
def sort_queue_by_digit(q,i):
  """ setřídí frontu čísel 'q' dle i-té číslice """  
  prihradka=[ ListQueue() for j in range(10) ]
  while not q.is_empty():
    x=q.dequeue()
    c=digit(x,i) # číslice pro třídění
    prihradka[c].enqueue(x)
  r=ListQueue()
  for p in prihradka:
    r.concatenate(p)
  return r  

def radix_sort_inplace(a): # třídění na místě
  a[:]=radix_sort_array_integers(a)

# --------------------- testovací část --------------------------

import random
import sorting_experiments


def main():

    # ukázka  
    a=[random.randrange(100) for i in range(10)]
    print(a)
    print(radix_sort_array_integers(a))

def test():
    # kontrola na mnoha náhodných vstupech
    sorting_experiments.test_sort(f=radix_sort_inplace)  

def timing():    
    # měření času
    import time
    from radix_sort_experiments import radix_sort_integers as radix_sort_array
    a=[random.randrange(10000) for i in range(1000000)]
    t0=time.clock()
    a1=radix_sort_array(a)
    t1=time.clock()
    q=array_to_queue(a)
    t2=time.clock()
    q2=radix_sort_queue_integers(q)
    t3=time.clock()
    print("radix_sort_array: ",t1-t0, "  radix_sort_queue_integers:", t3-t2)

if __name__=="__main__":
  main()    
  test()
  timing()
