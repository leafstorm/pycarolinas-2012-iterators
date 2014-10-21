# fibogen.py

def fibonacci():
    yield 0
    yield 1
    a, b = 0, 1

    while True:
        a, b = b, a + b
        yield b

