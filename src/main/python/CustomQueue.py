# Custom Queue Implementation - It behaves like a set and only adds unique values
class MyQueue:

    def __init__(self):
        self.queue = list()

    # checks for an entry before adding it
    def enqueue(self, data):
        if data not in self.queue:
            self.queue.insert(0, data)
            return True
        return False

    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return ("Queue is Empty!")

    def size(self):
        return len(self.queue)

    def printQueue(self):
        return self.queue
