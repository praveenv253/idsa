#!/usr/bin/env python

"""
Program to convert an infix expression to a postfix expression using a stack.
"""

import sys

class Stack(object):
    """Simple implementation of a stack data type."""

    def __init__(self):
        self.stack = []

    def push(self, item):
        """Push an item onto the stack. No return value."""
        self.stack.append(item)

    def pop(self):
        """Pop the topmost item off the stack. Returns the item."""
        item = self.stack[-1]
        self.stack = self.stack[:-1]
        return item

    def peek(self):
        """
        Peek at the topmost item of the stack without popping. 
        Returns the item, or None on underflow.
        """
        try:
            return self.stack[-1]
        except IndexError:
            return None

    def is_empty(self):
        """Returns whether or not the stack is empty."""
        return len(self.stack) == 0

    def __len__(self):
        """Return number of items on the stack."""
        return len(self.stack)

    def __repr__(self):
        """String representation of the stack."""
        return str(self.stack)

# Expression error signalling some manner of error in the input expression
class ExpressionError(Exception):
    """Class to raise errors in the input expression."""
    pass

def validate(string):
    """
    Validates that the string is a correct infix expression. 
    Also, replaces unary minus operators with a 'u-'.
    
    Returns a valid, tokenized string on success; raises ExpressionError if the
    input is erroneous.
    """
    
    tokens = string.split()
    
    # Remembers if the previous token was an operator
    opflag = True
    
    ## Highly inefficient validity checking begins here ##
    
    # List of operators as they would appear in the infix expression
    operators = ['+', '-', '*', '/', '^', 'sqrt']
    
    # First and foremost, detect all unary minus signs and mark them as such
    for i in xrange(len(tokens)):
        # A unary minus is a minus operator which occurs after another operator
        # or after an open parenthesis.
        if tokens[i] in operators or tokens[i] == '(':
            if opflag:
                if tokens[i] == '-':
                    tokens[i] = 'u-'
                    # Leave opflag true to allow cascading of unary minuses
                elif tokens[i] in ['sqrt', '(']:
                    # These operators can be cascaded, so leave them alone
                    # Also, leave opflag true to handle a subsequent u-
                    pass
                else:
                    # Any other operator must be caught
                    raise ExpressionError('Operators cannot be cascaded!')
            # We found an operator, but opflag isn't true. Set it.
            else:
                opflag = True
        else:
            # We found something other than an operator, or a ')'. If opflag is
            # false, and the token is not ')', then we have two adjacent
            # variables/numbers. This is also an invalid combination
            if not opflag and tokens[i] != ')':
                raise ExpressionError('Adjacent operands with no operator!')
            # Otherwise, unset opflag
            else:
                opflag = False
    
    # Check whether parentheses match
    s = Stack()
    for token in tokens:
        if token == '(':
            s.push(token)
        elif token == ')':
            if s.pop() != '(':
                raise ExpressionError('Parentheses do not match')
    if not s.is_empty():
        raise ExpressionError('Parentheses do not match')
    
    return tokens

def infix_to_postfix(string):
    """
    Function to convert a single input infix string to postfix notation.
    It is assumed that tokens in the string are separated by whitespace.
    
    Returns the postfix expression on success; raises ExpressionError if the
    input expression is erroneous.
    """
    
    # Validate and tokenize the string
    tokens = validate(string)
    
    # Initialize the stack
    s = Stack()

    # Ready the final postfix expression
    postfix = ''
    
    # List of operators that have to be handled
    operators = ['+', '-', '*', '/', '^', 'sqrt', 'u-', '(', ')']
    
    # Iterate through tokens
    for token in tokens:
        if token in operators:
            if token in ['sqrt', 'u-']:
                # Square root and unary minus have the highest precendence. So
                # they get pushed on to the stack immediately
                s.push(token)
            elif token == '^':
                top = s.peek()
                while top in ['sqrt', 'u-']:
                    postfix += s.pop() + ' '
                    top = s.peek()
                s.push(token)
            elif token in ['*', '/']:
                # Multiplication and division have the same precedence. Order
                # is determined by order of appearance
                top = s.peek()
                while top in ['sqrt', 'u-', '^']:
                    postfix += s.pop() + ' '
                    top = s.peek()
                s.push(token)
            elif token in ['+', '-']:
                # Addition and subtraction have the same precedence. Order is
                # determined by order of appearance
                top = s.peek()
                while top in ['sqrt', 'u-', '^', '*', '/']:
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
        else: # Token is a number or variable
            postfix += token + ' '

    # Pop out any more operators that might be sitting on the stack
    while(len(s)):
        postfix += s.pop() + ' '

    # Get rid of trailing whitespace and print
    postfix = postfix.strip()
    return postfix

if __name__ == '__main__':
    # Acquire infix strings from input
    for line in sys.stdin.readlines():
        try:
            output = infix_to_postfix(line.replace('\n', '').replace('\r', ''))
        except ExpressionError:
            print 'ERROR'
            continue
        else:
            print output
