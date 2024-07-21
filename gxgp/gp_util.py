#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP in pure Python
#    / \     To be used as a wireframe when teaching EAs
#  10   11   01URROV Computational Intelligence in PoliTO

import inspect
from typing import Callable

__all__ = ['arity']


def arity(f: Callable) -> int:
    """Return the number of expected parameter of the function"""
    return len(inspect.getfullargspec(f).args)
