"""
File: listqueue.py
Author: Man-Chi Leung
"""


class ListQueue(object):
    """An list-based stack implementation."""

    # Constructor
    def __init__(self, sourceCollection = None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self.items = []
        if sourceCollection:
            for item in sourceCollection:
                self.items.append(item)

    # Accessor methods
    def isEmpty(self):
        """Returns True if the queue is empty, or False otherwise."""
        return len(self) == 0
    
    def __len__(self):
        """Returns the number of items in the queue."""
        return len(self.items)

    def __str__(self):
        """Returns the string representation of the queue."""
        s = "{"
        for i in range(len(self.items)):
            s += str(self.items[i])
            if i < len(self.items) - 1:
                s += ", "
        s += "}"
        return s

    def __iter__(self):
        """Supports iteration over a view of the queue."""
        return (x for x in self.items)

    def __add__(self, other):
        """Returns a new queue containing the contents
        of self and other."""
        q = ListQueue(self)
        for item in other.items:
            q.add(item)
        return q

    def __eq__(self, other):
        """Returns True if self equals other,
        or False otherwise."""
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.items[i] != other.items[i]:
                return False
        return True

    def peek(self):
        """Returns the item at the front of the queue.
        Precondition: the queue is not empty.
        Raises IndexError if queue is empty."""
        if self.isEmpty():
            raise IndexError
        return self.items[0]

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self.items = []

    def add(self, item):
        """Inserts item at rear of the queue."""
        self.items.append(item)

    def pop(self):
        """Removes and returns the item at the front of the queue.
        Precondition: the queue is not empty.
        Raises IndexError if queue is not empty.
        Postcondition: the front item is removed from the queue."""
        if self.isEmpty():
            raise IndexError
        return self.items.pop(0)
