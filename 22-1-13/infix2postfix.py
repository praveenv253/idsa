#!/usr/bin/env python

"""
Program to convert an infix expression to a postfix expression using a stack.
"""

import sys
import re
from stack import Stack

# Expression error signalling some manner of error in the input expression
class ExpressionError(Exception):
    """Class to raise errors in the input expression."""
    pass

# Acquire string from program arguments
if len(sys.argv) != 2:
    print 'Insufficient number of command line parameters'
    print 'Usage: %s <expression>' % sys.argv[0]
    sys.exit(1)
string = sys.argv[1]

# Initialize the stack
s = Stack()

def tokenize(string):
    """
    Function that accepts an infix expression and tokenizes it. Removes stray
    spaces in the input string. Currently cannot handle negative numbers.
    
    Returns a list of tokens into which the argument string has been broken.
    Raises ExpressionError when the argument is an invalid infix expression.
    
    Examples:
    '25+10'            -> ['25', '+', '10']
    '4.1*( 71 +31.6) ' -> ['4.1', '*', '(', '71', '+', '31.6', ')']
    """
    
    tokens = []
    # Matches a floating point number
    number = re.compile('^((\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')
    # Matches a parenthesis
    paren = re.compile('^([()])')
    # Matches an operator
    operator = re.compile('^([+\-*/^])')
    
    # Kill all spaces in the string
    string = string.replace(' ', '').replace('\t', '')
    
    # Attempt to match possible tokens one by one
    while(string):
        found_match = False
        for regex in [number, paren, operator]:
            result = regex.match(string)
            if result:
                tokens.append(result.group(0))
                # Remove token once it has been identified
                string = string.split(result.group(0), 1)[1]
                found_match = True
                break
        if not found_match:
            # If we reach this point, then we have encountered an illegal token
            raise ExpressionError('Unidentified token in input expression')
    
    return tokens

# Call tokenize on the input string
tokens = tokenize(string)

# Ready the final postfix expression
postfix = ''

# Tokenize the string and iterate through contents
for token in tokens:
    try:
        # Numbers can immediately be put into the postfix expression
        float(token)
    except ValueError:
        if token == '^':
            top = s.peek()
            if top == '^':
                raise ExpressionError('Cascaded ^ operators causes ambiguity')
            s.push(token)
        # Multiplication and division have the same precedence. Order is
        # determined by order of appearance
        elif token in ['*', '/']:
            top = s.peek()
            while top in ['^', '*', '/']:
                postfix += s.pop() + ' '
                top = s.peek()
            s.push(token)
        # Addition and subtraction have the same precedence. Order is
        # determined by order of appearance
        elif token in ['+', '-']:
            top = s.peek()
            while top in ['^', '*', '/', '+', '-']:
                postfix += s.pop() + ' '
                top = s.peek()
            s.push(token)
        elif token == '(':
            s.push(token)
        elif token == ')':
            top = s.peek()
            while top != '(':
                postfix += s.pop() + ' '
                top = s.peek()
            s.pop()
        else:
            raise ExpressionError('Unrecognised token in expression')
    else: # Number worked out
        postfix += token + ' '

# Pop out any more operators that might be sitting on the stack
while(len(s)):
    postfix += s.pop() + ' '

# Get rid of trailing whitespace and print
postfix.strip()
print postfix
