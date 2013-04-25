#!/usr/bin/env python

def main():
    import sys
    import math
    
    f = {0: 1, 1: 1}
    def factorial(n):
        fact = 1
        for i in range(n, 0, -1):
            if i in f:
                return fact * f[i]
            else:
                fact *= i
                f[i] = fact
        
    # We don't care how many test cases there are. They keep throwing them at
    # us, we keep solving away.
    a = sys.stdin.readline()
    
    for line in sys.stdin.readlines():
        (N, k) = line.replace('\n', '').split()
        (N, k) = (int(N), int(k))
        
        if k == N:
            print(0)
            continue
        
        # Analytical solution is twice N-1 choose k.
        print(int((2 * factorial(N-1) // factorial(k) // factorial(N-1-k)) % 1000000007))

if __name__ == '__main__':
    main()
