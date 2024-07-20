#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP implementation in pure python
#    / \     To be used as a wireframe when teaching EAs
#  10   11   01URROV Computational Intelligence in PoliTO

from typing import Collection
import random

from .gp_util import arity

from .node import Node

__all__ = ['GP', 'evaluate']


class GP:
    def __init__(self, operators: Collection, variables: int | Collection, constants: int | Collection, *, seed=42):
        self.__random = random.Random(seed)
        self._operators = list(operators)
        if isinstance(variables, int):
            self._variables = [Node(GP.default_variable(i)) for i in range(variables)]
        else:
            self._variables = [Node(t) for t in variables]
        if isinstance(constants, int):
            self._terminals = [Node(self.__random.random()) for i in range(constants)]
        else:
            self._terminals = [Node(t) for t in constants]

    def create_individual(self, n_nodes=7):
        pool = self._variables + self._terminals
        individual = None
        while individual is None or len(individual) < n_nodes:
            op = self.__random.choice(self._operators)
            params = self.__random.choices(pool, k=arity(op))
            individual = Node(op, params)
            pool.append(individual)
        return individual

    @staticmethod
    def default_variable(i: int) -> str:
        return f'x{i}'


def evaluate(individual: Node, X, variable_names=None):
    if variable_names:
        names = variable_names
    else:
        names = [GP.default_variable(i) for i in range(len(X[0]))]

    y_pred = list()
    for row in X:
        y_pred.append(individual(**{n: v for n, v in zip(names, row)}))
    return y_pred


def evaluate_names(individual: Node, X):
    y_pred = list()
    for row in X:
        y_pred.append(individual(**row))
    return y_pred