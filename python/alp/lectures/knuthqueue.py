# -*- coding: utf-8 -*-
# Implementace třídy fronta (Queue) pomocí dvou zásobníků

# Jan Kybic

from alp.lectures.stack import Stack


class Queue:

    def __init__(self):
        self.inp = Stack()
        self.out = Stack()

    def is_empty(self):
        return self.size() == 0

    def enqueue(self, item):
        self.inp.push(item)

    def peek(self):
        self.check_out()
        return self.out.peek()

    def dequeue(self):
        self.check_out()
        return self.out.pop()

    def check_out(self):
        if self.out.is_empty():
            while not self.inp.is_empty():
                self.out.push(self.inp.pop())

    def size(self):
        return self.inp.size() + self.out.size()
