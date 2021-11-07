# Merge sort experiments
import random
import sorting_experiments



  
def merge_sort(a):
  """ Setřídí pole a pomocí merge sort """
  if len(a)<=1:   # triviální případ
    return a 
  mid=len(a)//2   # rozdělení pole na dvě
  left=merge_sort(a[:mid])
  right=merge_sort(a[mid:])
  return join_arrays(left,right)

def join_arrays(left,right):
  """ Dvě vzestupně setříděná pole spojí do jednoho """
  result=[] # spojení dvou setříděných polí
  i=0       # index do 'left'
  j=0       # index do 'right'

  while i<len(left) and j<len(right):
    if left[i]<right[j]:
      result+=[left[i]]
      i+=1
    else:
      result+=[right[j]]
      j+=1

  result+=left[i:]    # doplnit zbytky
  result+=right[j:]    
  return result


def merge_sort_inplace(a):
  """ merge_sort_inplace uloží výsledek do původního pole 'a' """
  a[:]=merge_sort(a)

def main():  
  print("merge sort")
  a=[random.randrange(100) for i in range(10)]
  print(a)
  print(merge_sort(a))

  sorting_experiments.test_sort(f=merge_sort_inplace)  

  sorting_experiments.time_sorting_algorithms(algs=[sorting_experiments.bubble_sort,
                                                  sorting_experiments.selection_sort,
                                                  sorting_experiments.insertion_sort,
                                                  merge_sort,sorting_experiments.python_sort],
                                                  prefix="time_with_mergesort")
if __name__=="__main__":
  main()    
