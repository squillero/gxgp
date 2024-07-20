#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP implementation in pure python
#    / \     To be used as a wireframe when teaching EAs
#  10   11   01URROV Computational Intelligence in PoliTO

import random
import operator

from icecream import ic
import gxgp

gp = gxgp.GP(operators=[operator.add, operator.sub, operator.mul],
             variables=2, constants=5, seed=42)
i = gp.create_individual(10)
ic(i.long_name)

X = list()
for _ in range(5):
    X.append([random.random() * 200 - 100 for _ in range(2)])
ic(X)
ic(gxgp.evaluate(i, X))

i.draw()
