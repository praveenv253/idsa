#!/usr/bin/env python

import sys
import heapq

# A graph shall be represented in adjacency list format:
# The set of vertices is a list, and each element of the list links to a list
# of tuples (other_node, weight, pointer to Q element)
# Apart from this, we also need to maintain a heap, in order to be able to
# quickly find the minimum current distance estimate
if __name__ == '__main__':
    
    num_test_cases = int(sys.stdin.readline().replace('\n', ''))
    
    for test_case_index in xrange(num_test_cases):
        # Number of vertices and edges
        v, k = sys.stdin.readline().split()
        v, k = int(v), int(k)
        
        # Trying out weird ways of implementing pointers in python
        # Cyclic references and all that!
        V = [[] for i in xrange(k)]           # Initialize empty adjacency list
        Q = [[10001, ()] for i in xrange(k)]  # Initialize heap for extractmin
                                              # Default distance estimate is
                                              # 10001, since data <= 10000
        for edge_index in xrange(k):
            i, j, w = sys.stdin.readline().split()
            i, j, w = int(i), int(j), int(w)
            V[i].append((j, w, Q[j]))
        
        a, b = sys.stdin.readline()
        a, b = int(a), int(b)
        
        for i in xrange(v):
            # Be careful not to replace the whole list!! V points to it!
            if i != a:
                Q[i][1] = V[i]
            else:
                # Source is at a distance of zero from itself
                Q[i][1] = V[i]
        
        # Now let's heapify Q. Ouch.
        heapq.heapify(Q)
        
        # Here starts Dijkstra
        while Q:
            # u is an element of Q, v is an element of an element of V
            u = heapq.heappop(Q)
            if u[1] is None:                    # In case the Qelem has been
                                                # removed
                continue
            for v in u[1]:
                # if d(src, v) > d(src, u) + w
                if v[2][0] > u[0] + v[1]:
                    newQelem = v[2][:]          # Create a copy of the Qelem
                                                # to modify
                    newQelem[0] = u[0] + v[1]
                    v[2][1] = None              # Remove the previous Qelem
                                                # by setting its node to None
                    v[2] = newQelem
                    heapq.heappush(newQelem)    # Add the new Qelem
        
        # Done with Dijkstra!
        
