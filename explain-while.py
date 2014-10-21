# is equivalent to this:

iterator = iter(container)
while True:
    try:
        item = iterator.next()
    except StopIteration:
        break
    else:
        do_something_with(item)

