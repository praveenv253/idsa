#!/usr/bin/env python

class TreeElem(object):
    """
    Class to contain a single node in a tree.
    Can link to other tree elements.
    """
    def __init__(self, value):
        self.value = value
        self.occurrences = 1


class BinarySearchTree(object):
    """
    Class to implement a binary search tree.
    Supports pre-order and post-order printing.
    """
    
    def __init__(self, value=None):
        if value is None:
            self.empty = True
        else:
            self.root = TreeElem(value)
            self.empty = False
    
    def insert(self, value):
        found = False
        loc = self.root
        while not found:
            if value > loc.value:
                try:
                    loc = loc.right
                except AttributeError:
                    loc.right = TreeElem(value)
                    found = True
            elif value < loc.value:
                try:
                    loc = loc.left
                except AttributeError:
                    loc.left = TreeElem(value)
                    found = True
            else:
                loc.occurrences += 1
                found = True
    
    @classmethod
    def _pre(cls, node):
        # It is expected that each node will have a value
        print node.value
        try:
            cls._pre(node.left)
        except AttributeError:
            pass
        try:
            cls._pre(node.right)
        except AttributeError:
            pass
    
    def preorder(self):
        if not self.empty:
            self._pre(self.root)
    
    @classmethod
    def _post(cls, node):
        try:
            cls._post(node.left)
        except AttributeError:
            pass
        try:
            cls._post(node.right)
        except AttributeError:
            pass
        # It is expected that each node will have a value
        print node.value
    
    def postorder(self):
        if not self.empty:
            self._post(self.root)
    
    @classmethod
    def _inorder(cls, node):
        try:
            cls._inorder(node.left)
        except AttributeError:
            pass
        # It is expected that each node will have a value
        for i in xrange(node.occurrences):
            print node.value
        try:
            cls._inorder(node.right)
        except AttributeError:
            pass
    
    def inorder(self):
        if not self.empty:
            self._inorder(self.root)


if __name__ == '__main__':
    import sys
    
    bst = BinarySearchTree()
    for line in sys.stdin.readlines():
        op = line.split()[0]
        if op == 'insert':
            value = float(line.split()[1])
            if bst.empty:
                bst = BinarySearchTree(value)
            else:
                bst.insert(value)
        elif op == 'print_sort':
            bst.inorder()
        elif op == 'print_pre':
            bst.preorder()
        elif op == 'print_post':
            bst.postorder()

