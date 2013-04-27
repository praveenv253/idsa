#!/usr/bin/env python

def main():
    import sys
    
    n, m = sys.stdin.readline().replace('\n', '').split()
    n, m = int(n), int(m)
    v = {}
    for i in xrange(m):
        a, b = sys.stdin.readline().replace('\n', '').split()
        a, b = int(a), int(b)
        if a in v:
            v[a][2].add(b)
        else:
            v[a] = [a, 0, set([b])]
        if b in v:
            v[b][2].add(a)
        else:
            v[b] = [b, 0, set([a])]
    
    print v
    
    d = []
    def dfs(a):
        print a[0]
        for i in a[2]:
            # Should not contract paths of length 1 and 2.
            if i in d and i != d[-1] and i != d[-2]:
                # Loop! Contract.
                index = d.index(i)
                b = set([])
                for j in d[index:]:
                    b.update(v[j][2])
                    v[j][2] = b
                del d[index:]
                d.append(a[0])
                dfs(a)
                continue
            # Only do a dfs if the node has not already been visited
            if v[i][1] == 0:
                d.append(i)
                v[i][1] = 1
                dfs(v[i])
    
    d.append(0)
    v[0][1] = 1
    dfs(v[0])
    
    print v[0]

if __name__ == '__main__':
    main()
