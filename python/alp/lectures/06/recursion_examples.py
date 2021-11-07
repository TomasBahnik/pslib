# Příklady na rekurzi
# Jan Kybic, 2016


# umocňování
print("power")

def power_iterative(x,n):
   prod=1.0
   for i in range(n):
      prod*=x
   return prod

print(power_iterative(2.0,10))


def power_recursive(x,n):
   if n<=0:
      return 1.0
   return x*power_recursive(x,n-1)

print(power_recursive(2.0,10))

def power_recursive2(x,n):
  return x*power_recursive2(x,n-1) if n>0 else 1.0

print(power_recursive2(2.0,10))


# součet pole
print("sum array")

def sum_array(a):
  s=0
  for x in a:
    s+=x
  return s

a=[68, 0, 61, 34, 2, 51, 29, 10, 5, 45]
print(sum_array(a))


def sum_array_recursive(a):
  if len(a)==0:
    return 0
  return a[0]+sum_array_recursive(a[1:])

print(sum_array_recursive(a))

# kazdy cyklus lze napsat pomoci rekurze
print("count to")

def count_to(n):
  for i in range(1,n+1):
    print(i)

count_to(5)
    
def count_to_recursive(n):
  count_to_recursive_inner(n,1)

def count_to_recursive_inner(n,i):
  if i<=n:
    print(i)
    count_to_recursive_inner(n,i+1)  

count_to_recursive(5)

def count_to_recursive2(n):
  def count_to_recursive_inner(i):
    if i<=n:
      print(i)
      count_to_recursive_inner(i+1)  
  count_to_recursive_inner(1)

count_to_recursive2(5)



      

# řetězec pozpátku

def reverse_iterative(s):
  r="" # result
  for i in range(len(s)-1,-1,-1):
    r+=s[i]
  return r

print(reverse_iterative("dobrý večer"))

def reverse_recursive(s):
  if len(s)==0:
    return ""
  return reverse_recursive(s[1:])+s[0]

def reverse_recursive2(s):
  return "" if  s=="" else reverse_recursive2(s[1:])+s[0]


print(reverse_recursive("dobrý večer"))
print(reverse_recursive2("dobrý večer"))

print("dobrý večer"[::-1])



# Mince - jak zaplatit danou částku mincemi daných hodnot
print("Mince")



def zaplat(x):
  """ vytiskni vsechny mozne zpusoby, jak zaplatit 'x'
  mincemi definovanych hodnot h """
  h=[50,20,10,5,2,1] # hodnoty mincí sestupně
  def doplat(x,m,i):
    """ m - kolik zaplaceno v poctech minci
        i - kterou minci zacit """
    if x==0:
      vytiskni_platbu(m,h)
    else: 
       if x>=h[i]: # zaplat minci h[i]
          doplat(x-h[i],m[:i]+[m[i]+1]+m[i+1:],i)
       if i<len(h)-1: # zaplat mensimi
          doplat(x,m,i+1)   
  doplat(x,len(h)*[0],0)


def vytiskni_platbu(m,h):
  """ m - pocty minci, h - hodnoty """
  for j in range(len(h)):
    if m[j]>0:
       print("%2d*%2dKč" % (m[j],h[j]), end="")
  print("")


zaplat(12)

def zaplat2(x):
  """ vytiskni vsechny mozne zpusoby, jak zaplatit 'x'
  mincemi definovanych hodnot h """
  h=[50,20,10,5,2,1] # hodnoty mincí sestupně
  def doplat(x,m,i):
    """ m - kolik zaplaceno v poctech minci
        i - kterou minci zacit """
    if x==0:
      vytiskni_platbu(m,h)
    else: 
       if x>=h[i]: # zaplat minci h[i]
          m[i]+=1
          doplat(x-h[i],m,i)
          m[i]-=1  # úklid
       if i<len(h)-1: # zaplat mensimi
          doplat(x,m,i+1)   
  doplat(x,len(h)*[0],0)

zaplat2(12)

  
# Převod do jiné číselné soustavy
print("Prevod do jiné číselné soustavy")

def to_str(n, base):
  """ Vrať 'n' jako řetězec v číselné soustavě se základem 'base' """
  assert(n>=0)
  cislice = "0123456789ABCDEF"
  if n < base:
    return cislice[n]
  return to_str(n // base, base) + cislice[n % base]

print(to_str(2016,16))
print(to_str(5,2))

def to_str_nonrecursive(n,base):
  assert(n>=0)
  cislice = "0123456789ABCDEF"
  stack=[n] # hodnoty n
  n//=base
  while n>0:
    stack+=[n]
    n//=base
  result=""
  for m in stack[::-1]:
    result+=cislice[m % base]
  return result

print(to_str_nonrecursive(2016,16))
print(to_str_nonrecursive(5,2))


def to_str_nonrecursive2(n,base):
  assert(n>=0)
  cislice="0123456789ABCDEF"
  result=""
  while True:
    result=cislice[n % base]+result
    n//=base
    if n==0: break
  return result

print(to_str_nonrecursive2(156,10))
print(to_str_nonrecursive2(2016,16))
print(to_str_nonrecursive2(5,2))


# Generování permutací
print("permutace")

def tisk_permutaci(m):
  """ Vytiskne všechny permutace prvků v 'm' """
  tisk_permutaci_acc(m,"")

def tisk_permutaci_acc(m,acc):
  if len(m)==0:
    print(acc,end=", ")  
  else:
    for i in range(len(m)):
      tisk_permutaci_acc(m[:i]+m[i+1:],acc+m[i]+" ")

tisk_permutaci(["a","b","c","d"])      



# Quick sort

# Radix sort
