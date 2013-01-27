"""
Program to evaluate a postfix expression using a stack.
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

def eval_rpn(string):
    """
    Evaluate a reverse polish notation expression using a stack.
    
    Returns the result of the evaluation.
    Raises ``ExpressionError`` if there is an error in the input expression.
    """
    
    # Initialize the stack
    s = Stack()
    
    # Tokenize the string and iterate through contents
    for token in string.split():
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
                        try:
                            subresult = operand1 / operand2
                        except ZeroDivisionError:
                            raise ExpressionError('Division by zero')
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
        # There shouldn't be any numbers left in the stack at this point
        raise ExpressionError('Too many numbers')
    try:
        # At the end, pop the result and return it
        result = s.pop()
        return result
    except IndexError:
        raise ExpressionError('Stack underflow, too few numbers')
    
if __name__ == '__main__':
    # Acquire string from program arguments
    for line in sys.stdin.readlines():
        try:
            output = eval_rpn(line.replace('\n', '').replace('\r', ''))
        except ExpressionError:
            print 'ERROR'
            continue
        else:
            print '%.4f' % output
