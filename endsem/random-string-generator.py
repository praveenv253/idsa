#!/usr/bin/env python

import random
import string

if __name__ == '__main__':
    a = string.ascii_letters
    #a = a.replace('a', '').replace('i', '').replace('e', '').replace('o', '').replace('u', '')
    for i in xrange(100000):
        maxj = random.randint(1, 10)
        maxj = 10
        for j in xrange(maxj):
            wordlen = random.randint(1, 10)
            wordlen = 10
            print ''.join(random.choice(a) for i in xrange(wordlen)),
        print
