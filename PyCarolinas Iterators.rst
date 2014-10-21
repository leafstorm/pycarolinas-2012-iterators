========================
Iterators and Generators
========================
:author:    Matthew Frazier
:date:      October 20, 2012

Hello, my name is Matthew Frazier, and I will be talking about iterators
and generators in Python.

(Brief discussion of qualifications.)

The examples in this talk will be given in Python 2. Python 3's iterator
protocol is mostly the same as 2's, so I will note any important distinctions
when necessary.

First Question
==============
The first question is, where do you find iterators?

I assume everyone is familiar with the basic ``for`` loop::

    >>> for food in ["egg", "bacon", "sausage"]:
    ...     print food + " and spam"
    egg and spam
    bacon and spam
    sausage and spam

In its most common form, you have some kind of collection type --
like a list, a set, or a dict -- in between the ``in`` and the ``:``,
and Python will store each item from the collection in the variable
you provide, then run the block of code.
This is referred to as, "iteration."

Besides collections, you can iterate over a lot of different things.
For example, this text file, containing lines from Macbeth::

    >>> macbeth = open("macbeth.txt")
    ... for line in macbeth:
    ...     print line.strip()
    ...
    When shall we three meet again
    In thunder, lightning, or in rain?
    When the hurlyburly's done,
    When the battle's lost and won.
    That will be ere the set of sun.
    Where the place?
    Upon the heath.
    There to meet with Macbeth.
    I come, Graymalkin!
    Paddock calls.
    >>> macbeth.close()

For loops aren't the only place you can use iterables.
Many data types, such as ``list`` and ``dict``, accept iterables when created.
Let's take ``set`` as an example::

    >>> letters = set("abracadabra")
    >>> print letters
    set(["a", "b", "r", "c", "d"])

It iterated over the word, and added each item to the set.
In this case, the items were letters, so each letter was added.

There are also functions that can work with any iterable.
While ``max`` is most often used to find the largest number in a list,
it also works for strings -- it will find the character in the string
that occurs latest in the character set. ::

    >>> max("abracadabra")
    'r'

Because you can use them and combine them in so many ways,
iterables are one of Python's most powerful features.
For example, we can take two files, with English and Spanish days
of the week, (show days-[english,spanish].txt, C-j 2)
and quickly convert them into a dictionary::

    >>> english = open("days-english.txt")
    >>> spanish = open("days-spanish.txt")
    >>> days = dict(zip(map(str.strip, english), map(str.strip, spanish)))
    {"monday": "lunes", "tuesday": "martes", ...}


The Iterable Protocol
=====================
How does this work, you might ask?
Let's take a look at a ``list``'s methods::

    >>> l = ["egg", "bacon", "sausage"]
    >>> dir(l)
    [..., '__iter__', ...]

All iterables have a special method named ``__iter__``.
It takes no arguments, and returns a different kind of object. ::

    >>> i = l.__iter__()
    >>> i
    <listiterator object at 0x...>

``listiterator`` isn't a type you can create instances of yourself.
It just serves as a helper object for ``list``.
Let's take a look at its methods::

    >>> dir(i)
    [..., '__iter__', ..., 'next']

It has an ``__iter__`` method as well!
What happens when we call it? ::

    >>> i.__iter__()
    <listiterator object at 0x...>
    >>> i.__iter__() is i
    True

It just returns itself.
But what's more interesting is the ``next`` method.
That's the only method ``listiterator`` has that most Python objects don't
have. ::

    >>> i.next()
    'egg'
    >>> i.next()
    'bacon'

Each time ``next`` is called, it returns the next item in the list.
However, the idea of the "next item" is unique to this ``listiterator``. ::

    >>> i2 = l.__iter__()
    >>> i is i2
    False
    >>> i2.next()
    'egg'
    >>> i.next()
    'sausage'
    >>> i2.next()
    'bacon'

``i2`` will return the same items over again, without ``i`` affecting it.

We're at the end of ``i`` now. So what happens when we run out of items?

    >>> i.next()
    Traceback (most recent call last):
        ...
    StopIteration

Awww... Maybe again?

    >>> i.next()
    Traceback (most recent call last):
        ...
    StopIteration

This iterator is completely exhausted.
And there's no way to rewind it.
But since ``i2`` hasn't iterated through the entire list yet,
it's still fine::

    >>> i2.next()
    'sausage'
    >>> i2.next()
    Traceback (most recent call last):
        ...
    StopIteration

Well, it *was*.


The Protocols
=============
``listiterator``s are part of a general kind of object known as an *iterator*.
Some iterators are created directly, but most of them are created from an
iterable, and you never see them otherwise.

The two protocols that govern iteration are the Iterable Protocol and the
Iterator Protocol.

The Iterable Protocol is simplest:
Any object with an ``__iter__`` method can be iterated over.
It should accept no methods, and return a *new* iterator object for the
iterable.
This iterator should be independent of any other iterators for that object.

The Iterator Protocol is slightly more complicated:
Iterators need to have ``__iter__`` and ``next`` methods.
The ``__iter__`` method should just return self.
This means that all iterators are iterables (sort of).

Iterators represent streams (or laundry chutes) of data.
Calling ``next`` returns the next item in the chute.
(When you have a fresh iterator, ``next`` returns the first item.)
After it has iterated through all of the items,
``next`` must raise a ``StopIteration`` exception every time it is called.
If it returns more items after the first time it raises ``StopIteration``,
it is *broken*.

When you put an object in a for loop, like this (C-j 3)::

    for item in container:
        do_something_with(item)

This is basically what happens::

    iterator = iter(container)
    while True:
        try:
            item = iterator.next()
        except StopIteration:
            break
        else:
            do_something_with(item)

(``iter`` is a function that usually just calls ``__iter__`` on its argument.
However, if the argument isn't actually an iterable, it will try a bit
of leftover magic from before Python 2.2 to create one on the fly.)

This means that iterables and iterators are mostly interchangeable as far
as for loops are concerned.


Writing our own iterator
========================
Iterators don't just iterate over containers, though. Take ``xrange``
for example::

    >>> for i in xrange(3):
    ...     print i
    0
    1
    2

There's not a container here, it just creates values based on some preset
criteria.

To demonstrate, I will create an iterator that iterates over the
Fibonacci sequence. (show fibonacci.py, C-j 4)

As you can see, the parent Fibonacci class is basically stateless --
all the state is kept in the iterators.

Let's give it a try:

    >>> from fibonacci import fibo
    >>> for n in fibo:
    ...     print n
    0
    1
    1
    2
    3
    5
    8
    ...
    Traceback (most recent call last):
        ...
    KeyboardInterrupt

That's another important thing about iterators:
they're not guaranteed to stop.

While it may seem like iterators which return infinite values are useless,
they have their uses.
We just need a good way to limit them down to a value we can use.
We can add a ``break`` to the loop once we have all we need::

    >>> for n in fibo:
    ...     if n >= 50: break
    ...     print n
    ...
    0
    1
    1
    2
    3
    5
    8
    13
    21
    34

But we might not be using it directly in a loop.
We might be passing it into a function like ``list``,
where we can't just add a ``break``.
(In fact, if you try ``list(fibo)``, it will lock up the Python process
and eat a bunch of RAM.)


Itertools
=========
The Python standard library has a module called ``itertools`` that has
a bunch of useful helpers for working with iterators.
One of them is ``takewhile``.

It accepts a predicate function, and an iterable, and returns an
iterator.
When you ask the ``takewhile`` iterator for its next item,
it will call ``next`` on the iterator inside,
and then it calls the predicate function.
If the predicate function returns True, it yields the returned value.
If the predicate function returns False, it stops iterating.

    >>> from fibonacci import fibo
    >>> from itertools import takewhile
    >>> for n in takewhile(lambda n: n < 20, fibo):
    ...     print n
    0
    1
    1
    2
    3
    5
    8
    13

That's much less screen-overflowing!

This also makes it useful for creating lists::

    >>> list(takewhile(lambda n: n < 20, fibo))
    [0, 1, 1, 2, 3, 4, 8, 13]


Composing Iterators
===================
While ``itertools`` ships with a ``takewhile``, it doesn't have a ``take``.
This is a common function in languages like Haskell and F#,
that will just grab a certain number of items before stopping.
Let's write one! (show take.py, C-j 5)

We can use it to grab the first six Fibonacci numbers, like this::

    >>> from take import take
    >>> for n in take(6, fibo):
    ...     print n
    0
    1
    1
    2
    3
    5

Because the iterator protocol is just based on methods,
we can create all kinds of iterators that manipulate other iterators.


Generators
==========
If you look at both ``take`` and ``fibonacci``, handling state is pretty
tricky.
Fortunately, there's a special kind of function, called a "generator,"
that can help with managing the state.

A generator is a function that can generate a sequence of results.
You can do the same thing with a function that returns a ``list`` or other
container type.
However, with those functions, you call the function,
generate the entire set of results,
and then return them back, all at once.
Generators, however, can stop after generating each result,
and then continue later.

Here's a simple generator to demonstrate::

    >>> def multiples(n):
    ...     m = 1
    ...     while True:
    ...         print "(m = %d)" % m
    ...         yield m * n
    ...         m = m + 1
    ...

Generators look just like normal functions,
except they have ``yield`` statements somewhere in the body.

However, when you call a generator, it accepts the arguments just like normal,
but it doesn't start running the function::

    >>> g = multiples(5)
    <generator object at 0x...>

Instead, it creates a generator object.
This generator object contains the function's locals, call stack, and all
that stuff.
We actually start the generator running by calling ``next``::

    >>> g.next()
    (m = 1)
    5

It started running the function, then paused when it reached the ``yield``.
The return value of ``next`` was the value we passed to ``yield``:
5, in this case.
However, the function is still alive.

If we continue to call ``next``, it will run through another iteration of the
``while`` loop.

    >>> g.next()
    (m = 2)
    10
    >>> g.next()
    (m = 3)
    15

It will keep running until the generator function returns, or dies because of
an exception.

We already know that generators have a ``next`` method.
They also have an ``__iter__``::

    >>> g.__iter__()
    <generator object at 0x...>
    >>> g.__iter__() is g
    True

Because the ``__iter__`` method of a generator returns itself,
all generator objects are iterators.
So we can use them in for loops.

    >>> for n in g:
    ...     print n
    ...
    (m = 4)
    20
    (m = 5)
    25
    (m = 6)
    30
    ...
    Traceback (most recent call last):
        ...
    KeyboardInterrupt

When the generator function returns, or an exception escapes it,
it will raise StopIteration, which will stop the for loop (if necessary).

And since the function is no longer running, calling ``next`` will have
no effect::

    >>> g.next()
    Traceback (most recent call last):
        ...
    StopIteration

However, you can call the generator function multiple times
to start the function over again::

    >>> for n in take(3, multiples(7)):
    ...     print n, "parrots"
    (m = 1)
    7 parrots
    (m = 2)
    14 parrots
    (m = 3)
    21 parrots

When the function returns,
the generator will automatically raise ``StopIteration`` for us.


Rewriting with Generators
=========================
If you look back at the Fibonacci code,
the trickiest aspect about it is keeping track of the state between calls
to ``next``.
We have to store any data that we want to remember between calls in instance
variables,
and if it's this much of a pain for a simple Fibonacci sequence...yeah.

But generators help us because we don't need to use instance variables to
remember our state, and rebuild it from scratch:
Python takes care of it for us. (show fibogen.py, C-j 6)

This code is much shorter, for one, and it has less boilerplate.
Another thing to note is that we can have multiple ``yield`` statements,
at different parts of the function.
This is good for the Fibonacci sequence,
since we have two "special cases" at the beginning (0 and 1),
and only get to the repetitive part after that.

Let's try it out::

    >>> from fibogen import fibonacci
    >>> list(take(6, fibonacci()))
    [0, 1, 1, 2, 3, 5]


Rewriting Take with Generators
==============================
We can also use generators to rewrite ``take``. (show takegen.py, C-j 7)

Notice that we don't need to catch StopIteration ourselves.
When the ``next`` of the child iterator raises StopIteration,
it will stop the generator for us.
We don't even have to worry about the child iterator being broken!


Applications of Generators
==========================
There's one other important thing about generators:
``yield`` isn't actually a statement. It's an expression.
This means we can do things with its return value.

    >>> def yieldexpr():
    ...     print "starting up..."
    ...     count = 0
    ...     while True:
    ...         value = yield count
    ...         print "yield returned", repr(value)
    ...         count = count + 1
    ...

``yield`` will return a value whenever the generator starts back up again.
When you call ``next``, or iterate through it with ``for``,
the return value is ``None``.

    >>> y = yieldexpr()
    >>> y.next()
    starting up...
    0
    >>> y.next()
    yield returned None
    1
    >>> y.next()
    yield returned None
    2

However, whoever holds the generator object can make ``yield`` return a
different value by calling the ``send(value)`` method on the generator. ::

    >>> y.send(True)
    yield returned True
    3
    >>> y.send("Hello!")
    yield returned 'Hello!'
    4

You can send any value into the generator, and ``yield`` will return it.
However, if you send any value that isn't ``None`` to the generator
before you start it, it explodes::

    >>> y2 = yieldexpr()
    >>> y2.send(5)
    Traceback (most recent call last):
        ...
    TypeError: can't send non-None value to a just-started generator

Thanks to this rule, ``next()`` is exactly the same as ``send(None)``.

There are two other methods you can use to mess with generators.
The first is ``throw(exc)``, which makes ``yield`` raise an exception
instead of returning a value.

    >>> y.throw(RuntimeError("stop"))
    Traceback (most recent call last):
        ...
    RuntimeError: stop

If the generator doesn't catch the exception,
it will die, and the exception will be sent right back to your code.
Then, the generator will be stopped.

    >>> y.next()
    Traceback (most recent call last):
        ...
    StopIteration

However, as with normal exceptions, the generator can catch it and
yield a value back to you anyway.

    >>> def catcher():
    ...     last_exc = None
    ...     while True:
    ...         try:
    ...             yield last_exc
    ...         except BaseException as e:
    ...             last_exc = e
    ...
    >>> c = catcher()
    >>> c.next()
    >>> c.throw(RuntimeError(3))
    RuntimeError(3,)
    >>> c.throw(RuntimeError("die"))
    RuntimeError('die',)

However, there's another method you can use that's guaranteed to kill a
generator.

    >>> y3 = yieldexpr()
    >>> y3.next()
    starting up...
    0
    >>> y3.close()

It works by creating an exception called ``GeneratorExit`` and throwing
it at the generator.
Usually, this will kill it.
However, if the generator catches the exception and yields a value anyway...

    >>> c.close()
    Traceback (most recent call last):
        ...
    RuntimeError: generator ignored GeneratorExit

Our code gets the exception instead.


Applications of Advanced Generators
===================================
So...why are these useful?
We can use them to implement coroutines.

Who here knows Tornado? (wait for hands)
Tornado is a framework for asynchronous network programming.
Asynchronous programming lets you handle lots of connections at the same time,
because it doesn't use threads or multiple processes.
However, it requires that you write code that look like this:
(show C-j 8)

You have to use callbacks for everything.
This can make your code hard to follow,
since you're have to move from one function to another
every time you need to wait for something.

However, the newly introduced ``tornado.gen`` module
allows you to write code that looks like normal synchronous code,
even though it's really asynchronous behind the scenes: (show C-j 9)

In this particular implementation,
``gen.engine`` is decorates generators.
It lets your generator yield ``gen.Task`` objects.
These hold a function and some arguments.
Tornado will call the function with those arguments,
and a special callback that calls the generator's ``send`` method
with the results of the asynchronous call.

This means that even though several seconds may pass,
and other things may happen,
from your code's perspective, it was just waiting on a response like normal.
But in reality, Tornado could have been serving dozens of other requests
at the same time.

Right now, the Tornado API isn't fully integrated with ``gen``.
But it's fairly easy to write some wrappers,
so you could forget that you were using ``gen`` at all.


Conclusion
==========
Thank you for listening to my presentation!
If you're interested in more about what you can do with iterators,
I recommend that you read the PEPs where all these features were designed.
(C-j l)
