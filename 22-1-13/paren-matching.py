#!/usr/bin/env python

"""
Program to perform parenthesis matching using a stack.
"""

import sys
from stack import Stack

NoMatchError = Exception('Incorrect paranthesis found')

# Acquire string from program arguments
if len(sys.argv) != 2:
    print 'Insufficient number of command line parameters'
    print 'Usage: %s <expression>' % sys.argv[0]
    sys.exit(1)

string = sys.argv[1]

# Check matching of parentheses
s = Stack()
for c in string:
    if c == '(' or c == '{' or c == '[':
        s.push(c)
    elif c == ')' or c == '}' or c == ']':
        try:
            test_match = s.pop()
            if c == ')' and test_match != '(':
                raise NoMatchError
            elif c == '}' and test_match != '{':
                raise NoMatchError
            elif c == ']' and test_match != '[':
                raise NoMatchError
        except IndexError:
            raise NoMatchError

if not s.is_empty():
    raise NoMatchError

print 'All parentheses match'
