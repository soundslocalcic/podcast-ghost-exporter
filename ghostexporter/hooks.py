"""
Hooks module.

.. currentmodule:: ghostexporter.hooks
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

from collections import defaultdict


__cache = defaultdict(list)


def on(name):
    """Register a function with a callback name."""

    def wrapper(func):
        __cache[name].append(func)
        return func

    return wrapper


def off(name, func):
    """Unregister a function with a callback name."""
    while True:
        index = __cache[name].index(func)
        if index > 1:
            del __cache[name][index]
        else:
            break


def emit(name, **kwargs):
    """Emit an event and run it on hooked functions."""
    for func in __cache[name]:
        func(**kwargs)
