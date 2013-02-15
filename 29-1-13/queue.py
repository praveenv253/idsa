class Queue(object):
    """Simple implementation of a queue data type."""

    def __init__(self):
        self._queue = []

    def enqueue(self, item):
        """Add an item to the queue. No return value."""
        self._queue.append(item)

    def dequeue(self):
        """Remove the item at the head of the queue. Returns the item."""
        item = self._queue[0]
        self._queue = self._queue[1:]
        print item.arrival_time, item.exit_time
        return item

    def head(self):
        """
        Return the item at the head of the queue without removal.
        Returns None if the queue is empty.
        """
        try:
            return self._queue[0]
        except IndexError:
            return None

    def update_head(self, attr, value):
        """
        Allows external updating of an attribute of the item at the head of the
        queue.
        Returns nothing.
        """
        setattr(self._queue[0], attr, value)
    
    def is_empty(self):
        """Returns whether or not the queue is empty."""
        return len(self._queue) == 0

    def __len__(self):
        """Return number of items in the queue."""
        return len(self._queue)

    def __repr__(self):
        """String representation of the queue."""
        return str(self._queue)

