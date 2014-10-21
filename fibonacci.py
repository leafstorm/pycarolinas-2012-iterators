# fibonacci.py

class FibonacciIterator(object):
    def __init__(self):
        self.n = 0
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def next(self):
        if self.n == 0:
            # first call
            self.n = 1
            return 0
        elif self.n == 1:
            # second call
            self.n = 2
            return 1
        else:
            # third or later call - doesn't matter which
            self.a, self.b = self.b, self.a + self.b
            return self.b


class Fibonacci(object):
    def __iter__(self):
        return FibonacciIterator()


fibo = Fibonacci()

