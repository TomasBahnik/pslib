# -*- coding: utf-8 -*-
# příklad na použití zásobníku
from stack import Stack

s=Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())
print(s.pop())
s.push(10)
print(s.pop())
print(s.is_empty())
print(s.pop())
print(s.is_empty())

def to_str(n,base):
  """ Převede číslo 'n' na řetězec pro soustavu se základem 'base' """
  cislice = "0123456789ABCDEF"
  assert(n>=0)
  stack=Stack()
  while True:
    stack.push(n % base)
    n//=base
    if n==0:
      break
  result=""
  while not stack.is_empty():
    result+=cislice[stack.pop()]
  return result

print(to_str(67,2))

import random

def quick_sort(a):
  """ Setřídí pole a na místě """
  stack=Stack()
  stack.push((0,len(a)-1))
  while not stack.is_empty():
      (first,last)=stack.pop()
      m = partition(a,first,last)
      if first<m-1:
          stack.push((first,m-1))
      if m+1<last:
          stack.push((m+1,last))

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

a=[random.randrange(100) for i in range(10)]
quick_sort(a)
print(a)


###############################################################

def par_checker(s):  
   """ returns True if the string 's' is correctly parenthesized """
   lparens="([{"  # otevírací závorky
   rparens=")]}"  # uzavírací závorky (ve stejném pořadí)
   stack=Stack()
   for c in s:
     if c in lparens:
       stack.push(c)
     for i in range(len(rparens)):
       if c==rparens[i]:
         if stack.is_empty() or stack.pop()!=lparens[i]: # líné vyhodnocení
           return False
   return stack.is_empty()

print(par_checker("(4+(3*[a+b]))"))
print(par_checker("(x+([21*c]-5}*6)"))
print(par_checker("[(3+4)*7-{}*(((0)+(1))%7)]"))
print(par_checker("{ { ( [ ] [ ] ) } ( ) }"))
print(par_checker("ahoj+(svete-(X+Y{}})"))

###############################################################

def eval_postfix(s):
   """ returns the value of a postfix expression given by a string 's'"""
   stack=Stack()
   for x in s.split(): # rozděl 's' dle mezer
     if x=='+':
       stack.push(stack.pop()+stack.pop())
     elif x=='-':
       stack.push(-stack.pop()+stack.pop())
     elif x=='*':
       stack.push(stack.pop()*stack.pop())
     elif x=='/':
       second=stack.pop()
       stack.push(stack.pop()/second)
     else:
       stack.push(float(x))
   return stack.pop()    

# python evaluates expressions left to right       
# there is no error checking

print(eval_postfix("3 4 *"))
print(eval_postfix("10 6 -"))
print(eval_postfix("20 4 /"))
print(eval_postfix("3 4 * 2 -")) # 3 * 4 - 2
print(eval_postfix("3 4 2 - *")) # 3 * (4 - 2)

###############################################################

def infix_to_postfix(s):
  """ converts an infix to postfix expression """
  result=""  # output string
  op=Stack() # operator stack
  i=0        # index to 's'
  while i<len(s):
    if s[i] in "0123456789":
      while i<len(s) and s[i] in  "0123456789":
        result+=s[i]
        i+=1
      result+=" "
      continue   
    if s[i]=='(':
      op.push(s[i])
    elif s[i]==')':
      top=op.pop()
      while top!='(': 
        result+=top+" "
        top=op.pop()    
    else: # s[i] is +,-,*,/
      while not op.is_empty() and not higher_prec(s[i],op.peek()):
        result+=op.pop()+" "
      op.push(s[i])
    i+=1           
  while not op.is_empty():
     result+=op.pop()+" "
  return result

def higher_prec(a,b):
  """ does operator 'a' have a higher precedence than the stack top element 'b' """
  return ((a in "*/") and (b in "+-")) or (b=="(")

print(infix_to_postfix("32+4"))
print(infix_to_postfix("3*4-2"))
print(infix_to_postfix("3*(4-2)"))
print(infix_to_postfix("(62-32)*5/9"))

def eval_infix(s):
  return eval_postfix(infix_to_postfix(s))

print(eval_infix("32+4"))
print(eval_infix("3*4-2"))
print(eval_infix("3*(4-2)"))
print(eval_infix("(62-32)*5/9"))

# nekontroluje, nesmi tam byt mezery

  

