# Creating binary tree
# from given list
# conda install binarytree -c conda-forge
from binarytree import build

# List of nodes
nodes = [21, 16, 19, 87, 34, 92, 66]

# Building the binary tree
binary_tree = build(nodes)
print('Binary tree from list :\n',
      binary_tree)

# Getting list of nodes from
# binarytree
print('\nList from binary tree :',
      binary_tree.values)
