# takegen.py

def take(n, iterable):
    iterator = iter(iterable)

    for i in range(n):
        # if the child raises StopIteration,
        # it will cascade up
        yield iterator.next()

