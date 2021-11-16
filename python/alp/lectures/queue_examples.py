# -*- coding: utf-8 -*-
# příklad na použití zásobníku
#from slowqueue import Queue
from knuthqueue import Queue
#from arrayqueue import Queue

import random

q=Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q.dequeue())
print(q.dequeue())
q.enqueue(10)
print(q.dequeue())
print(q.is_empty())
print(q.dequeue())
print(q.is_empty())

def stress_test_queue():
  for j in range(10):
    print("j=",j)
    for i in range(1000000):
      q.enqueue(i)

    for i in range(1000000):
      q.dequeue()  

#stress_test_queue()      

def merge_sort(a):
  """ Setřídí pole 'a' pomocí merge sort """
  q=Queue()
  for x in a:
    q.enqueue(x)
  q=merge_sort_queue(q)
  for i in range(q.size()):
    a[i]=q.dequeue()
  return a
    
def merge_sort_queue(q):
  """ Setřídí frontu 'q' pomocí merge sort """
  if q.size()<=1:   # triviální případ
    return q 
  m=q.size()//2     # počet prvků po rozdělení
  left=Queue()
  for i in range(m):
    left.enqueue(q.dequeue())
  left=merge_sort_queue(left)
  right=merge_sort_queue(q)
  return join_queues(left,right)

def join_queues(left,right):
  """ Dvě vzestupně setříděné fronty spojí do jedné """
  result=Queue() # výsledek

  while not left.is_empty() and not right.is_empty():
    if left.peek()<right.peek():
      result.enqueue(left.dequeue())
    else:
      result.enqueue(right.dequeue())

  while not left.is_empty(): # doplnit zbytky
      result.enqueue(left.dequeue())
  while not right.is_empty():
      result.enqueue(right.dequeue())

  return result

a=[random.randrange(100) for i in range(10)]
print(a)
print(merge_sort(a))
