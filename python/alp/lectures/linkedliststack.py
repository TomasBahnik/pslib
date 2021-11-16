# -*- coding: utf-8 -*-
# Implementace spojového seznamu podporujícího operace zásobníku
#
# Jan Kybic, 2016

class Node:   # uzel
  def __init__(self,data):
    self.data = data
    self.next = None # odkaz na další uzel

class ListStack:   # seznam
  def __init__(self):
    self.head = None

  def is_empty(self):
    return self.head is None

  def push(self,item):
    node=Node(item)
    node.next=self.head
    self.head=node

  def pop(self):
    item=self.head.data
    self.head=self.head.next
    return item
    
  def peek(self):  
    return self.head.data
