#!/usr/bin/env python

def main():
    import sys
    
    count = 0
    
    # Relies on average-case constant access time of the dictionary.
    # http://wiki.python.org/moin/TimeComplexity
    a = {}
    
    # O(n)
    for line in sys.stdin.readlines():
        line = line.replace('\n', '')
        val = int(line)
        a[val] = 1
    
    # Loop (without internals) has O(n^2) steps
    # Internals involves checking if an item is present in the dictionary, plus
    # some constant time arithmetic.
    # Checking whether an item is present is again O(1), in the average case.
    # So the overall loop is still O(n^2).
    l = len(a)
    for i in a:
        for j in a:
            if i <= j:
                continue
            if i * j in a:
                count += 1
    
    print int(count)

if __name__ == '__main__':
    main()

