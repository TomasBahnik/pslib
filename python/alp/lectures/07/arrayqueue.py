# -*- coding: utf-8 -*-
# Implementace třídy fronta (Queue) s postupnou alokací

# Jan Kybic


class Queue:

  def __init__(self):
    self.front = 0
    self.items = []
  def is_empty(self):
    return len(self.items) == self.front
  def enqueue(self, item):
    self.items+=[item]
  def dequeue(self):
    el=self.items[self.front]
    self.front+=1
    if self.front >= 1024 and self.front>=len(self.items)//2:
       # print("Compactify", len(self.items), self.front)
       self.items=self.items[self.front:]
       self.front=0
    return el
  def size(self):
    return len(self.items)
