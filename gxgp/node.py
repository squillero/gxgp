#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP implementation in pure python
#    / \     To be used as a wireframe when teaching EAs
#  10   11   01URROV Computational Intelligence in PoliTO


from typing import Callable
import numbers

from .gp_util import *

__all__ = ['Node']


class Node:
    _func: Callable
    _children: tuple['Node']
    _arity: int
    _leaf: bool
    _str: str

    def __init__(self, node=None, children=None, *, name=None):
        if callable(node):
            def _f(*_args, **_kwargs):
                return node(*_args)

            self._func = _f
            self._children = tuple(children)
            self._arity = arity(node)
            assert len(tuple(children)) == arity(
                node), "Panik: Incorrect number of children." + f" Expected {len(tuple(children))} found {arity(node)}"
            self._leaf = False
            self._children = tuple(children)
            if name is not None:
                self._str = name
            elif node.__name__ == '<lambda>':
                self._str = 'λ'
            else:
                self._str = node.__name__
        elif isinstance(node, numbers.Number):
            self._func = eval(f'lambda **_kw: {node}')
            self._children = list()
            self._arity = 0
            self._leaf = True
            self._str = str(node)
        elif isinstance(node, str):
            self._func = eval(f'lambda *, {node}, **_kw: {node}')
            self._children = list()
            self._arity = 0
            self._leaf = True
            self._str = str(node)
        else:
            assert False

    def __call__(self, **kwargs):
        return self._func(*[c(**kwargs) for c in self._children], **kwargs)

    def __str__(self):
        return self.short_name

    def __len__(self):
        return 1 + sum(len(c) for c in self._children)

    @property
    def value(self):
        return self()

    @property
    def arity(self):
        return self._arity

    @property
    def is_leaf(self):
        return self._leaf

    @property
    def short_name(self):
        return self._str

    @property
    def long_name(self):
        if self.is_leaf:
            return self.short_name
        else:
            return f'{self.short_name}(' + ', '.join(c.long_name for c in self._children) + ')'

    @property
    def subtree(self):
        return Node._get_subtree_nodes(self)

    def draw(self):
        import networkx as nx
        from networkx.drawing.nx_pydot import graphviz_layout

        G = nx.DiGraph()
        for n1 in list(self.subtree):
            G.add_node(n1)
            for n2 in list(n1._children):
                G.add_edge(n1, n2)
        pos = graphviz_layout(G, prog="dot")  # dot neato twopi circo fdp sfdp
        return nx.draw(
            G,
            pos=pos,
            # labels={k: str(k) for k in G},
            node_size=500,
            node_color='pink',
        )

    @staticmethod
    def _get_subtree_nodes(node: 'Node'):
        result = set()
        Node._get_nodes(result, node)
        return result

    @staticmethod
    def _get_nodes(bunch: set, node: 'Node'):
        bunch.add(node)
        for c in node._children:
            Node._get_nodes(bunch, c)
