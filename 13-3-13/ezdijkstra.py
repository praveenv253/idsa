#!/usr/bin/env python

import heapq

class Node(object):
    """
    Class to contain a single node in a graph.
    Can link to other graph nodes.
    """
    
    def __init__(self, label):
        self.label = label
        self.adj = []
        self.d = 10001             # estimated shortest distance from source
        self.parent = None      # parent in the shortest path
    
    @staticmethod
    def heapq_cmp_lt(x, y):
        return x.d < y.d
    
    def __cmp__(self, other):
        return cmp(self.label, other.label)
    
    def __repr__(self):
        return '(%d, %d)' % (self.label, self.d)


def contains(l, f):
    for x in l:
        if f(x):
            return True
    return False


class Graph(object):
    """
    Class to implement a graph.
    """
    
    def __init__(self):
        self.nodes = []
        heapq.heapify(self.nodes)
    
    def add_edge(a, b, w):
        """Add an edge between nodes a and b with a weight w."""
        if a == b:
            raise ValueError
        node_a = Node(a)
        if node_a not in self.nodes:
            heapq.heappush(self.nodes, node_a)
        else:
            for node in self.nodes:
                if node.label == a:
                    node_a = node
                    break
            node_a = self.nodes[self.nodes.index(a)]
        if not contains(self.nodes, lambda x: x.label == b):
            heapq.heappush(self.nodes, Node(b))
        node_a.adj.append((b, w))
    
    def dijkstra(s, t):
        

if __name__ == '__main__':
    import sys
    
    # Redefine comparison operator to use distance between nodes
    heapq.cmp_lt = Node.heapq_cmp_lt
    
    num_test_cases = int(sys.stdin.readline().replace('\n', ''))
    
    for test_case in xrange(num_test_cases):
        g = Graph()
        v, k = sys.stdin.readline().replace('\n', '').split()
        v, k = int(v), int(k)
        for edge in xrange(k):
            a, b, w = sys.stdin.readline().replace('\n', '').split()
            a, b, w = int(a), int(b), int(w)
            g.add_edge(a, b, w)
        s, t = sys.stdin.readline().replace('\n', '').split()
        s, t = int(s), int(t)
        print g.dijkstra(s, t)
