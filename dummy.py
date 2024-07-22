#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP in pure Python
#    / \
#  10   11   Distributed under MIT License

import random
import operator
import math
from dataclasses import dataclass

from gxgp import GP


@dataclass
class TestSet:
    X: list[list]
    y: list

    def __init__(self):
        self.X = list()
        self.y = list()


ts = TestSet()

for _ in range(1000):
    x = random.random() * 100
    y = math.sin(x)
    ts.X.append([x])
    ts.y.append(y)

gp = GP(operators=[operator.add, operator.sub, operator.mul],
        variables=1, constants=5, seed=42)

best = None
for _ in range(10):
    i = gp.create_individual(10)
    e = gp.mse(i, ts.X, ts.y)
    if best is None or e < best:
        best = e
        ic(e, str(i))
