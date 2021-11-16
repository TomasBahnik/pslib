# -*- coding: utf-8 -*-
# Implementace spojového seznamu podporujícího operace zásobníku a fronty + size()
#
# Jan Kybic, 2016

from linkedliststack import Node,ListStack
    
class ListQueue(ListStack):   # zdědíme ListStack
  def __init__(self):
    self.head = None
    self.last = None # last item
    self.count = 0

  def size(self):
    return self.count
          
  def push(self,item):   # přidej na začátku
    node=Node(item)
    node.next=self.head
    if self.head is None:
      self.last=node
    self.head=node
    self.count+=1
    
  def pop(self):         # odeber ze začátku
    item=self.head.data
    self.head=self.head.next
    if self.head is None:
      self.last=None
    self.count-=1
    return item

  def dequeue(self):
    return self.pop()
  
  def enqueue(self,item): # přidej na konec
    node=Node(item)
    if self.head is None: # seznam je prázdný
      self.head=node
      self.last=node
    else:
      self.last.next=node
      self.last=node
    self.count+=1      

  def concatenate(self,l):
    """ přidej seznam 'l' na konec tohoto seznamu, 'l' je vyprázdněn"""
    if l.last is None:
      return
    if self.last is None:
      self.head=l.head
    else:
      self.last.next=l.head
    self.last=l.last
    self.count+=l.count
    l.head=None # smaž list 'l'
    l.last=None
    l.count=0
    
  def iter(self,f):
    """ execute f(x) for all elements 'x' in the queue """
    node=self.head
    while node is not None:
      f(node.data)
      node=node.next
  
  def reduce(self,f,acc):
    """ execute acc=f(x,acc) for all elements 'x' in the queue, return 'acc' """
    node=self.head
    while node is not None:
      acc=f(node.data,acc)
      node=node.next
    return acc

  def to_array(self):
    a=[]
    self.iter(lambda x: a.append(x))  
    return a  

  def contains(self,x):
    """ returns True if the list contains element x """
    node=self.head
    while node is not None:
      if node.data==x:
        return True
      node=node.next
    return False

  def remove(self,x):
    """ removes an element x, if present """
    node=self.head
    prev=None 
    while node is not None:
      if node.data==x:
        if prev is None:
          self.head=node.next
          if self.head is None:
            self.last=None
        else:
          prev.next=node.next
      prev=node
      node=node.next

        
def array_to_queue(a):
  q=ListQueue()
  for x in a:
    q.enqueue(x)
  return q

