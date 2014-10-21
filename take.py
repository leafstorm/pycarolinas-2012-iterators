# take.py

class TakeIterator(object):
    def __init__(self, limit, iterator):
        self.limit = limit
        self.count = 0
        self.iterator = iterator

    def __iter__(self):
        return self

    def next(self):
        self.count = self.count + 1
        if self.count > self.limit:
            raise StopIteration
        # if the child iterator returns StopIteration,
        # it will cascade up
        return self.iterator.next()


def take(limit, iterable):
    return TakeIterator(limit, iter(iterable))

