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

        Q = [[float('inf'), i] for i in xrange(v)]  # Heap for extractmin
        V = [[] for i in xrange(v)]     # Initialize empty adjacency list
        Qdict = {}                      # Used to get the ith node's info
        Vdict = {}
        for i in xrange(v):
            Qdict[i] = Q[i]             # Create pointers to ith node
            Vdict[i] = V[i]
        for edge_index in xrange(k):
            i, j, w = sys.stdin.readline().split()
            i, j, w = int(i), int(j), int(w)
            i -= 1
            j -= 1
            V[i].append((j, w))

        a, b = sys.stdin.readline().split()
        a, b = int(a), int(b)
        a -= 1
        b -= 1

        Qdict[a][0] = 0

        # Now let's heapify Q. Ouch.
        heapq.heapify(Q)

        # Here starts Dijkstra
        while Q:

            # u and v are elements of Q
            u = heapq.heappop(Q)
            node_index = u[1]
            if node_index < 0:                  # Check if the node index is a
                                                # valid one
                continue

            # Iterate through adjacent nodes
            for adj_node in Vdict[node_index]:
                adj_node_index = adj_node[0]
                v = Qdict[adj_node_index]       # Adjacent node's dist estimate
                if v[0] > u[0] + adj_node[1]:   # if d(src, v) > d(src, u) + w
                    v_new = v[:]                # Create a copy of the Q elem
                                                # to modify
                    v_new[0] = u[0] + adj_node[1]
                    v[1] = -1                   # Remove the previous Q elem by
                                                # setting its node index to -1
                    Qdict[adj_node_index] = v_new
                    heapq.heappush(Q, v_new)    # Add the new Qelem

        # Done with Dijkstra!

        min_dist = Qdict[b][0]
        if min_dist < float('inf'):
            print min_dist
        else:
            print 'NO'

