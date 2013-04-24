#!/usr/bin/env python

def main():
    import sys
    from bisect import bisect_left
    
    # http://docs.python.org/2/library/bisect.html#searching-sorted-lists
    def contains(a, x):
        """Locate the leftmost value exactly equal to x"""
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        return -1

    count = 0
    a = []
    
    for line in sys.stdin.readlines():
        line = line.replace('\n', '')
        val = int(line)
        i = bisect_left(a, val)
        a.append(val)
        a[i+1:] = a[i:-1]
        a[i] = val
    
    l = len(a)
    for i in xrange(l-1):
        j = i
        while j < l:
            index = contains(a, a[i] * a[j])
            if index != -1:
                count += 1
            j += 1
    
    print count

if __name__ == '__main__':
    main()

