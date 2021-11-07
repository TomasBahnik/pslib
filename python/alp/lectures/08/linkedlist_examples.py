# -*- coding: utf-8 -*-
# příklady na použití spojového seznamu

from linkedliststack import ListStack

print("Stack")
s=ListStack()
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

from linkedlistqueue import ListQueue, array_to_queue

print("Queue")
q=ListQueue()
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

q=ListQueue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
r=ListQueue()
r.enqueue(4)
r.enqueue(5)
q.concatenate(r)
print(q.to_array())
while not q.is_empty():
  print(q.dequeue(),end=", ")
print()

#############################
# Vyhledávání v poli
q=array_to_queue([3,52,69,17,19])
print(q.contains(17))
print(q.contains(20))
#############################
# Smazání prvků v poli
q=array_to_queue([3,2,5,8,11])
q.remove(5)
print(q.to_array())
q.remove(3)
print(q.to_array())
q.remove(11)
print(q.to_array())
q.remove(16)
print(q.to_array())
q.remove(2)
print(q.to_array())
q.remove(4)
print(q.to_array())
q.remove(8)
print(q.to_array())
q.remove(8)
print(q.to_array())


#############################


