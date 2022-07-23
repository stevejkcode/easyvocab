import functools

# Various utility functions

# Decorator to wrap a given function and create a new function with no input params
# Needed for some things that require a function with no inputs (anki background tasks, etc)
def wrap_nonary(func):
    def outter(*args, **kwargs):
        @functools.wraps(func)
        def inner():
            return func(*args, **kwargs)
        return inner
    return outter