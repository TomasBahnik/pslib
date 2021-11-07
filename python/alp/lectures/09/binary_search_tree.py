# Implementace binárního vyhledávacího stromu
#
# Jan Kybic, 2016


class BinarySearchTree:
  def __init__(self, key,value=None,left=None,right=None):
    self.key = key
    self.value = value # None pro množinu
    self.left = left
    self.right = right

def print_tree(tree,level=0,prefix=""):
  if tree:
    if tree.value:
      print(" "*(4*level)+prefix+str(tree.key)+" -> "+str(tree.value))
    else:
      print(" "*(4*level)+prefix+str(tree.key))
    if tree.left:
      print_tree(tree.left,level=level+1,prefix="L:")
    if tree.right:
      print_tree(tree.right,level=level+1,prefix="R:")


def from_array(a):
  """ Build a tree (containing only keys) from an array """
  def build(a):
    if len(a)==0:
      return None
    if len(a)==1:
      return BinarySearchTree(a[0])
    m=len(a)//2
    return BinarySearchTree(a[m],left=build(a[:m]),right=build(a[m+1:]))  
  a=sorted(a)
  return build(a)

def contains(tree,key):
    """ Je prvek 'key' ve stromu? """
    if tree:            # je strom neprázdný?
      if tree.key==key: # je to hledaný klíč?
        return True
      if tree.key>key:
        return contains(tree.left,key)
      else:
        return contains(tree.right,key)
    return False
          
def get(tree,key):
    """ Vrátí 'value' prvku s klíčem 'key', jinak None """
    if tree:            # je strom neprázdný?
      if tree.key==key: # je to hledaný klíč?
        return tree.value
      if tree.key>key:
        return get(tree.left,key)
      else:
        return get(tree.right,key)
    return None
  
def add(tree,key):
  """ Vloží 'key' do stromu a vrátí nový kořen """
  if tree is None:
    return BinarySearchTree(key)
  if key<tree.key:
    tree.left=add(tree.left,key)
  elif  key>tree.key:
    tree.right=add(tree.right,key)
  return tree # hodnota již ve stromu je

def put(tree,key,value):
  """ Vloží pár 'key'->'value' do stromu a vrátí nový kořen """
  if tree is None:
    return BinarySearchTree(key,value=value)
  if key<tree.key:
    tree.left=put(tree.left,key,value)
  elif  key>tree.key:
    tree.right=put(tree.right,key,value)
  else:
    tree.value=value # klíč již ve stromu je
  return tree 

  
def to_array(tree):
  a=[]
  def insert_inorder(t):
    nonlocal a 
    if t:
      insert_inorder(t.left)
      a+=[t.key]
      insert_inorder(t.right)
  insert_inorder(tree)
  return a      

def rightmost_node(tree):
  """ returns the rightmost node of a tree """
  while tree.right:
    tree=tree.right
  return tree  
  
def delete(tree, key):
  """ Smaže 'key' za stromu 'tree' a vrátí nový kořen. """
  if tree is not None:
    if key < tree.key: # najdi uzel 'key'
      tree.left = delete(tree.left, key)
    elif key > tree.key:
      tree.right = delete(tree.right, key)
    else: # uzel nalezen, má syny?
      if tree.left is None:
        return tree.right # jen pravý syn nebo nic
      elif tree.right is None:
        return tree.left # jen levý syn nebo nic
      else: # nahradíme uzel maximem levého podstromu
        w = rightmost_node(tree.left)
        tree.key = w.key  
        tree.left = delete(tree.left, w.key)
  return tree

def minimum(tree):
  """ returns the minimum key """
  while tree.left:
    tree=tree.left
  return tree.key

def set_difference(x,y):
  """ Find elements in array 'y' but not in array 'x'. 
      WARNING: Assumes that 'y' is randomly ordered """
  t=None
  for i in y:
    t=add(t,i)
  for j in x:
    t=delete(t,j)
  return to_array(t)

# -------- test a demo -----

def test_tree():
  """ vyzkoušíme konstrukci pole, vyhledávání, přidávání prvků, tisk """
  t=from_array([21, 16, 19, 87, 34, 92, 66])
  print_tree(t)
  print(contains(t,30))
  print(contains(t,66))
  t=add(t,41)
  t=add(t,16)
  print_tree(t)
  
import random
  
def test_set():
  """ Vypíše všechny možné součty bodů na dvou kostkách """
  s=None
  for i in range(1000):
    s=add(s,random.randrange(1,7)+random.randrange(1,7))
  print_tree(s)
  print(to_array(s))  

def test_delete():
  t=from_array([21, 16, 19, 87, 34, 92, 66])
  print("test_delete")
  print_tree(t)
  t=delete(t,87)
  print_tree(t)


def permutation(n):
    "Create a random permutation of integers 0..n-1"
    p=list(range(n))
    for i in range(n-1):
       r=random.randrange(i,n)
       temp=p[r]
       p[r]=p[i]
       p[i]=temp
    return(p)

def two_random_subsets(n=100):
  x=[ random.randrange(1000) for i in range(n) ]
  y=x+[random.randrange(100)]
  y=[ y[i] for i in permutation(n+1)]
  return x,y

def test_set_difference():
  x,y=two_random_subsets(100)
  print(x)
  print(y)
  z=set_difference(x,y)
  print(z)

def test_map():
  t=None
  t=put(t,'pi',   3.14159)
  t=put(t,'e',    2.71828) 
  t=put(t,'sqrt2',1.41421)
  t=put(t,'golden',1.61803)
  print_tree(t)
  print(get(t,'pi'))
  print(get(t,'e'))
  print(get(t,'gamma'))
      
if __name__=="__main__":
  test_tree()    
  test_set()    
  test_delete()
  test_set_difference()
  test_map()
