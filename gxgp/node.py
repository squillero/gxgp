class Node:
    _func: Callable
    _children: tuple['Node']
    _arity: int
    _leaf: bool
    _str: str

    def __init__(self, node, children=None, *, name=None):
        if callable(node):
            def _f(*_args, **_kwargs):
                return node(*_args)

            self._func = _f
            self._children = tuple(children)
            self._arity = len(inspect.getfullargspec(node).args)
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

    @property
    def value(self):
        return self()

    @property
    def arity(self):
        return self._arity

    @property
    def is_leaf(self):
        return self._leaf

    def __str__(self):
        if self.is_leaf:
            return self._str
        else:
            return f'{self._str}(' + ', '.join(str(c) for c in self._children) + ')'

    @staticmethod
    def get_nodes(node: Node):
        result = set()
        Node._get_nodes(result, node)
        return result

    @staticmethod
    def _get_nodes(bunch: set, node: Node):
        bunch.add(node)
        for c in node._children:
            Node._get_nodes(bunch, c)
