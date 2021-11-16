# Quick sort experiments

import random
import sorting_experiments

def quick_sort(a):
  """ Setřídí pole a na místě """
  quick_sort_helper(a,0,len(a)-1)

def quick_sort_helper(a,first,last):
  """ setřídí podpole a[first]..a[last] """ 
  if first < last:
      m = partition(a,first,last)
      #print("Partition finished with a=",a," m=",m)
      quick_sort_helper(a,first,m-1)
      quick_sort_helper(a,m+1,last)

def partition(a,first,right):
  """ Vrátí index 'i' a změní 'a' tak, že všechny prvky před 'i' jsou menší než a[i] a všechny prvky po 'i' jsou větší než a[i]"""
  pivot=a[first]
  left=first+1
  #print("Calling partition with a=",a," first=",first," right=",right," pivot=",pivot)
  while True:
    # najdi první zleva větší než pivot
    while left<=right and a[left] <= pivot:
      left+=1
    while left<=right and a[right] >= pivot:
      right-=1
    if right<left:
      a[first],a[right]=a[right],a[first]  # pivot na místo
      return right
    a[left],a[right]=a[right],a[left] # výměna

def main():
    a=[random.randrange(100) for i in range(10)]
    print(a)
    quick_sort(a)
    print(a)

    sorting_experiments.test_sort(f=quick_sort)  

    import merge_sort_experiments
    sorting_experiments.time_sorting_algorithms(algs=[sorting_experiments.bubble_sort,
                                                      sorting_experiments.selection_sort,
                                                      sorting_experiments.insertion_sort,
                                                      merge_sort_experiments.merge_sort,
                                                      quick_sort,sorting_experiments.python_sort],
                                                      prefix="time_with_quicksort")

if __name__=="__main__":
  main()    
    
