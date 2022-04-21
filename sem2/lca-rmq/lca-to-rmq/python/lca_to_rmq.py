import random
from dataclasses import dataclass
from math import log2, ceil

@dataclass
class Node:
    '''
    Неявный ключ - позиция i
    Приоритет - A[i], приоритеты упорядочены от малого к большему
    Если минимальных A[i] несколько, то берем любой
    '''
    #key: int
    priority: int
    #num: int
    left: 'typing.Any' = None
    right: 'typing.Any' = None
    size: int = 1
    
    def __repr__(self):
        s = f'({self.priority}, {self.size}, left:{self.left}, right:{self.right})'
        return s
        s = ''
        if self.left is not None:
            s += self.left.__repr__()
        #s += f'({self.key},{self.priority}) '
        
        if self.right is not None:
            s += self.right.__repr__()
        return s
        
    def print_array(self):
       
       if self.left is not None:
           self.left.print_array()
       print(self.priority, end=' ')
       if self.right is not None:
           self.right.print_array()

    def __getitem__(self, i: int):
        if i > self.size:
            raise Exception('out of index bounds')
        if i == size_of(self.left):
            return self
        if i  < size_of(self.left):
            return self.left[i]
        else:
            return self.right[i - size_of(self.left) - 1]

def split(tree: Node, key):
    if tree is None:
        return None, None
    cur_index = size_of(tree) - 1
    if key >= cur_index:
        tree_1, tree_2 = split(tree.right, key - cur_index)
        tree.right = tree_1
        update(tree)
        return tree, tree_2
    else:
        tree_1, tree_2 = split(tree.left, key)
        tree.left = tree_2
        update(tree)
        return tree_1, tree
    
def merge(tree_left, tree_right):
    #print(f'left: {tree_left}')
    #print(f'right: {tree_right}')
    if not tree_left:
        return tree_right
    if not tree_right:
        return tree_left
    
    if tree_left.priority > tree_right.priority:
        #tree = tree_left
        tree_left.right = merge(tree_left.right, tree_right)
        update(tree_left)
        return tree_left
    else:
        #tree = tree_right
        tree_right.left = merge(tree_left, tree_right.left)
        update(tree_right)
        return tree_right

def insert_1(tree, node, pos):
        if not tree:
            return node
        #print(f'insert: {tree}, {node}')
        tree_1, tree_2 = split(tree, pos)
        tree_1 = merge(tree_1, node)
        
        tree = merge(tree_1, tree_2)
        print('!', tree_1)
        return tree

def insert_2(tree, node, pos):
    if not tree:
        return node
    if node.priority < tree.priority: 
        node.left, node.right = split(tree, pos+1)
        update(node)
        return node
    if pos < size_of(tree): #!!!
        tree.left = insert_2(tree.left, node, pos)
        update(tree)
    else:
        tree.right = insert_2(tree.right, node, pos)
        update(tree)
    return tree

def size_of(tree):
    return 0 if tree is None else tree.size

def update(tree):
    tree.size = size_of(tree.left) + size_of(tree.right) + 1


def dfs(u: int, parent: int):
    global curr_time
    curr_time += 1
    time_in[u] = curr_time
    parents[u][0] = parent
    for k in range(1, ceil(log2(n)) + 1):
        parents[u][k] = parents[parents[u][k - 1]][k - 1]

    if tree[u].left:
        dfs(u - size_of(tree[u].left.right) - 1, u)
    if tree[u].right:
        dfs(u + size_of(tree[u].right.left) + 1, u)
    curr_time += 1
    time_out[u] = curr_time
    
def is_upper(u: int, v: int) -> bool:
    return time_in[u] <= time_in[v] and time_out[u] >= time_out[v]

def lca(u: int, v: int) -> int:
    if is_upper(u, v): return u
    if is_upper(v, u): return v
    for k in range(ceil(log2(n)), -1, -1):
        if not is_upper(parents[u][k], v):
            u = parents[u][k]
    return parents[u][0]

    
