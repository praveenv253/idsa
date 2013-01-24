#!/usr/bin/env python

"""
Program to evaluate a postfix expression using a stack.
"""

import sys
from stack import Stack

# Expression error signalling some manner of error in the input expression
class ExpressionError(Exception):
    pass

# Acquire string from program arguments
if len(sys.argv) != 2:
    print 'Insufficient number of command line parameters'
    print 'Usage: %s <expression>' % sys.argv[0]
    sys.exit(1)
string = sys.argv[1]

# Initialize the stack
s = Stack()

# Tokenize the string and iterate through contents
for token in string.split(' '):
    try:
        # Numbers are to be pushed into the stack
        num = float(token)
    except ValueError:
        # Operators are immediately used to operate upon stacked numbers
        if token in ['+', '-', '*', '/', '^']:
            try:
                # Pop the two topmost numbers...
                operand2 = s.pop()
                operand1 = s.pop()
            except IndexError:
                raise ExpressionError('Stack underflow, too few numbers')
            else:
                # ...and operate on them
                if token == '^':
                    subresult = operand1 ** operand2
                elif token == '/':
                    subresult = operand1 / operand2
                elif token == '*':
                    subresult = operand1 * operand2
                elif token == '+':
                    subresult = operand1 + operand2
                elif token == '-':
                    subresult = operand1 - operand2
                s.push(subresult)
        else:
            raise ExpressionError('Undefined token in expression')
    else:
        s.push(num)

if len(s) > 1:
    raise ExpressionError('Too many numbers')
try:
    # At the end, pop the result and print it
    result = s.pop()
    print result
except IndexError:
    raise ExpressionError('Stack underflow, too few numbers')

