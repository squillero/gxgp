#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP in pure Python
#    / \
#  10   11   Distributed under MIT License

import inspect
from typing import Callable
import warnings
import numbers

from .gp_util import *

__all__ = ['Node']


class Node:
    _func: Callable
    _successors: tuple['Node']
    _arity: int
    _str: str

    def __init__(self, node=None, successors=None, *, name=None):
        if callable(node):
            def _f(*_args, **_kwargs):
                return node(*_args)

            self._func = _f
            self._successors = tuple(successors)
            self._arity = arity(node)
            assert len(tuple(successors)) == arity(
                node), "Panic: Incorrect number of children." + f" Expected {len(tuple(successors))} found {arity(node)}"
            self._leaf = False
            assert all(isinstance(s, Node) for s in successors), "Panic: Successors must be `Node`"
            self._successors = tuple(successors)
            if name is not None:
                self._str = name
            elif node.__name__ == '<lambda>':
                self._str = 'λ'
            else:
                self._str = node.__name__
        elif isinstance(node, numbers.Number):
            self._func = eval(f'lambda **_kw: {node}')
            self._successors = tuple()
            self._arity = 0
            self._str = f'{node:g}'
        elif isinstance(node, str):
            self._func = eval(f'lambda *, {node}, **_kw: {node}')
            self._successors = tuple()
            self._arity = 0
            self._str = str(node)
        else:
            assert False

    def __call__(self, **kwargs):
        return self._func(*[c(**kwargs) for c in self._successors], **kwargs)

    def __str__(self):
        return self.long_name

    def __len__(self):
        return 1 + sum(len(c) for c in self._successors)

    @property
    def value(self):
        return self()

    @property
    def arity(self):
        return self._arity

    @property
    def successors(self):
        return list(self._successors)

    @successors.setter
    def successors(self, new_successors):
        assert len(new_successors) == len(self._successors)
        self._successors = tuple(new_successors)

    @property
    def is_leaf(self):
        return not self._successors

    @property
    def short_name(self):
        return self._str

    @property
    def long_name(self):
        if self.is_leaf:
            return self.short_name
        else:
            return f'{self.short_name}(' + ', '.join(c.long_name for c in self._successors) + ')'

    @property
    def subtree(self):
        return Node._get_subtree_nodes(self)

    def draw(self):
        try:
            return self._draw()
        except Exception as msg:
            warnings.warn(f"Drawing not available ({msg})", UserWarning, 2)
            return None

    def _draw(self):
        import networkx as nx
        from networkx.drawing.nx_pydot import graphviz_layout

        G = nx.DiGraph()
        for n1 in list(self.subtree):
            for n2 in list(n1._successors):
                G.add_edge(id(n1), id(n2))

        pos = graphviz_layout(G, prog="dot")  # dot neato twopi circo fdp sfdp
        # plt.figure()
        # plt.title(self.long_name)

        nx.draw_networkx_nodes(
            G,
            nodelist=[id(n) for n in self.subtree if not
            n.is_leaf],
            pos=pos,
            node_size=800,
            node_color='lightpink',
            node_shape='o'  # so^>v<dph8
        )
        nx.draw_networkx_nodes(
            G,
            nodelist=[id(n) for n in self.subtree if
                      n.is_leaf and len(inspect.getfullargspec(n._func).kwonlyargs) == 1],
            pos=pos,
            node_size=500,
            node_color='lightgreen',
            node_shape='s'  # so^>v<dph8
        )
        nx.draw_networkx_nodes(
            G,
            nodelist=[id(n) for n in self.subtree if
                      n.is_leaf and len(inspect.getfullargspec(n._func).kwonlyargs) == 0],
            pos=pos,
            node_size=500,
            node_color='lightblue',
            node_shape='s'  # so^>v<dph8
        )
        nx.draw_networkx_labels(
            G,
            pos=pos,
            labels={id(n): n.short_name for n in self.subtree},
        )
        nx.draw_networkx_edges(
            G,
            pos=pos,
            node_size=800,
        )

    @staticmethod
    def _get_subtree_nodes(node: 'Node'):
        result = set()
        Node._get_nodes(result, node)
        return result

    @staticmethod
    def _get_nodes(bunch: set, node: 'Node'):
        bunch.add(node)
        for c in node._successors:
            Node._get_nodes(bunch, c)
