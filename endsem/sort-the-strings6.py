#!/usr/bin/env python

def main():
    import sys
    
    def merge(x, y):
        i = 0
        j = 0
        c = 0
        lx = len(x)
        ly = len(y)
        b = [0] * (lx + ly)
        while i < lx and j < ly and c < (lx + ly):
            if x[i][0] > y[j][0]:
                b[c] = y[j]
                j += 1
            else:
                b[c] = x[i]
                i += 1
            c += 1
        if i == lx:
            b[c:] = y[j:]
        else:
            b[c:] = x[i:]
        return b
    
    def mergesort(a):
        l = len(a)
        if l <= 1:
            return a
        x = a[:l/2]
        y = a[l/2:]
        x = mergesort(x)
        y = mergesort(y)
        a = merge(x, y)
        return a
    
    strings = []
    for line in sys.stdin.readlines():
        s = line.replace('\n', '')
        vowels = 0
        for i in s:
            if i in 'aeiouAEIOU':
                vowels += 1
        a = s.split()
        words = len(a)
        max_word_len = 0
        for word in a:
            if len(word) > max_word_len:
                max_word_len = len(word)
        strings.append(([vowels, words, max_word_len], s))
    
    #strings = mergesort(strings)
    
    for string in strings:
        print string[1]
    
if __name__ == '__main__':
    main()

