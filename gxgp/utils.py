#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP in pure Python
#    / \
#  10   11   Distributed under MIT License

import inspect
from typing import Callable

__all__ = ['arity']


def arity(f: Callable) -> int:
    """Return the number of expected parameter of the function"""
    return len(inspect.getfullargspec(f).args)
