#!/usr/bin/env python

import psyco
psyco.full()

# A graph shall be represented in adjacency list format:
# The set of vertices is a list, and each element of the list links to a list
# of tuples (other_node, weight, pointer to Q element)
# Apart from this, we also need to maintain a heap, in order to be able to
# quickly find the minimum current distance estimate
def main():    
    import sys
    import heapq
    
    while(1):
        # Number of vertices and edges
        v_, b, c, n, k = sys.stdin.readline().split()
        v_, b, c, n, k = int(v_), int(b), int(c), int(n), int(k)
        if [v_, b, c, n, k] == [-1, -1, -1, -1, -1]:
            break
        
        b -= 1
        c -= 1
        n -= 1
        
        Q = []                          # Initialize empty heap
        V = []                          # Initialize empty vertex list
        Qdict = []                      # Used to get the ith node's info
        Vdict = []
        for i in xrange(v_):
            Qelem = [float('inf'), i]   # Heap for extractmin operation
            heapq.heappush(Q, Qelem)
            V.append([])          # Initialize empty adjacency lists
            Qdict.append(Qelem)         # Create pointers to ith node
            Vdict.append(V[i])
        for edge_index in xrange(k):
            # Assume no multiple edges in input
            i, j, w = sys.stdin.readline().split()
            i, j, w = int(i), int(j), int(w)
            i -= 1
            j -= 1
            # Undirected graph => add both directions
            V[i].append((j, w))
            V[j].append((i, w))
        
        Qdict[b][0] = 0
        
        # Here starts Dijkstra (starting from bar)
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
        
        # Done with Dijkstra from bar!
        
        c_min_dist = Qdict[c][0]
        n_min_dist = Qdict[n][0]
        
        # Now to do Dijkstra starting from Charly's house
        
        C = []                          # Re-initialize empty heap
        Cdict = []                      # Used to get the ith node's info
        for i in xrange(v_):
            Celem = [float('inf'), i]   # Heap for extractmin operation
            heapq.heappush(C, Celem)
            Cdict.append(Celem)         # Create pointers to ith node
        
        Cdict[c][0] = 0
        
        while C:
            
            # u and v are elements of Q
            u = heapq.heappop(C)
            node_index = u[1]
            if node_index < 0:                  # Check if the node index is a
                                                # valid one
                continue
            
            # Iterate through adjacent nodes in the parent tree
            for adj_node in Vdict[node_index]:
                adj_node_index = adj_node[0]
                v = Cdict[adj_node_index]       # Adjacent node's dist estimate
                if v[0] > u[0] + adj_node[1]:   # if d(src, v) > d(src, u) + w
                    v_new = v[:]                # Create a copy of the Q elem
                                                # to modify
                    v_new[0] = u[0] + adj_node[1]
                    v[1] = -1                   # Remove the previous Q elem by
                                                # setting its node index to -1
                    Cdict[adj_node_index] = v_new
                    heapq.heappush(C, v_new)    # Add the new Qelem
        
        # Done with Dijkstra starting from Charly's house.
        
        # Now to do Dijkstra starting from Nito's house
        
        N = []                          # Re-initialize empty heap
        Ndict = []                      # Used to get the ith node's info
        for i in xrange(v_):
            Nelem = [float('inf'), i]   # Heap for extractmin operation
            heapq.heappush(N, Nelem)
            Ndict.append(Nelem)         # Create pointers to ith node
        
        Ndict[n][0] = 0
        
        while N:
            
            # u and v are elements of Q
            u = heapq.heappop(N)
            node_index = u[1]
            if node_index < 0:                  # Check if the node index is a
                                                # valid one
                continue
            
            # Iterate through adjacent nodes in the parent tree
            for adj_node in Vdict[node_index]:
                adj_node_index = adj_node[0]
                v = Ndict[adj_node_index]       # Adjacent node's dist estimate
                if v[0] > u[0] + adj_node[1]:   # if d(src, v) > d(src, u) + w
                    v_new = v[:]                # Create a copy of the Q elem
                                                # to modify
                    v_new[0] = u[0] + adj_node[1]
                    v[1] = -1                   # Remove the previous Q elem by
                                                # setting its node index to -1
                    Ndict[adj_node_index] = v_new
                    heapq.heappush(N, v_new)    # Add the new Qelem
        
        # Done with Dijkstra starting from Nito's house.
        
        split_point = None
        for v in xrange(v_):
            if ( Qdict[v][0] + Cdict[v][0] != c_min_dist or 
                 Qdict[v][0] + Ndict[v][0] != n_min_dist    ):
                continue
            if split_point is None:
                split_point = v
            elif (Qdict[split_point][0] < Qdict[v][0]):
                split_point = v
        
        print Qdict[split_point][0], Cdict[split_point][0], Ndict[split_point][0]


if __name__ == '__main__':
    main()
