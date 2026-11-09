def adder(*args, **kwargs):
    result = 0
    for n in args:
        result += n
    for m in kwargs.values():
        result += m
    return result

