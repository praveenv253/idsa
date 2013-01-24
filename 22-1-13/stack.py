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

