#!/usr/bin/env python

import random
import sys

try:
    num = int(sys.argv[1])
except:
    print 'Incorrect command line parameters'
    print 'Usage: %s <number of random numbers>' % sys.argv[0]

for i in xrange(num):
    print 'insert ' + str(random.random())

print 'print_sort'
    
