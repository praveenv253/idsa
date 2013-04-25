#!/usr/bin/env python

def main():
    import sys
    
    d = {}
    def func(i, j):
        # i = number of binary bits left in the stream
        # j = number of toggles left
        if j == 0:
            # No more toggles left. We have to make all bits here on in either
            # zero or one.
            return 2
        if i == j + 1:
            # Okay, that's it. We'll have to toggle every single time from now
            # on, in order to achieve j.
            # So there's only two possible ways of doing this. Either start
            # with a zero now, and then keep toggling, or start with a one now.
            return 2
        
        if i in d:
            if j in d[i]:
                return d[i][j]
        # Now we can decide whether to toggle or not. If we toggle, then both
        # i and j reduce by 1. If we don't toggle, i reduces by 1, but j doesnt
        val = (func(i-1, j-1) + func(i-1, j)) % 1000000007
        if i in d:
            d[i][j] = val
            return val
        else:
            d[i] = {j: val}
            return val
    
    # We don't care how many test cases there are. They keep throwing them at
    # us, we keep solving away.
    a = sys.stdin.readline()
    
    for line in sys.stdin.readlines():
        (N, k) = line.replace('\n', '').split()
        (N, k) = (int(N), int(k))
        
        if k == N:
            print(0)
            continue
        
        print(func(N, k))

if __name__ == '__main__':
    main()

