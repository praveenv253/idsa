#!/usr/bin/env python

count = 0

def main():
    import sys
    
    sys.setrecursionlimit(100000000)

    n, m = sys.stdin.readline().replace('\n', '').split()
    n, m = int(n), int(m)
    v = {}
    for i in xrange(m):
        a, b = sys.stdin.readline().replace('\n', '').split()
        a, b = int(a), int(b)
        if a in v:
            v[a][2].append(b)
        else:
            #       index, parent,       adj list, children, preorder label
            v[a] = [a,     float('inf'), [b],      [],       float('inf'), 
            #       ND(v), L(v),         H(v),
                    0,     float('inf'), -1,   ]
        if b in v:
            v[b][2].append(a)
        else:
            v[b] = [b, float('inf'), [a], [], float('inf'), 0, float('inf'), -1]
    
    #print v

    def dfs(a):
        global count
        # Set preorder label
        a[4] = count
        count += 1
        for i in a[2]:
            if v[i][1] == float('inf'):
                # Set parent
                v[i][1] = a[0]
                # Add child
                a[3].append(i)
                dfs(v[i])
        # Set number of descendants
        a[5] = sum([v[x][5] for x in a[3]]) + 1
        # Compute L(v)
        a[6] = a[4]         # Default value is its own preorder label
        searchspace = []
        for x in a[3]:
            # L(w)'s of a's children
            searchspace.append(v[x][6])
            # Preorder labels of the neighbours of the children
            # Don't include self in neighbours
            searchspace.extend([ v[i][4] for i in v[x][2] if i != a[0] ])
        if searchspace:
            a[6] = min(searchspace)
        # Compute H(v)
        a[7] = a[4]         # Default value is its own preorder label
        searchspace = []
        for x in a[3]:
            # H(w)'s of a's children
            searchspace.append(v[x][7])
            # Preorder labels of the neighbours of the children
            searchspace.extend([ v[i][4] for i in v[x][2] if i != a[0] ])
        if searchspace:
            a[7] = max(searchspace)
        #print a
        if a[4] == a[6] and a[7] < a[4] + a[5] and a[3] and a[0]:
            y = a[0]
            z = a[1]
            if y < z:
                print y, z
            else:
                print z, y
    
    # Create spanning tree
    v[0][1] = -1
    dfs(v[0])

if __name__ == '__main__':
    main()
