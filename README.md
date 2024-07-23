# GX's Genetic Programming

#### *A no-nonsense GP in pure Python*

```python
from gxgp import Node

tree = Node(operator.mul, [Node(operator.add, [Node(10),
                                               Node('x')]),
                           Node(2)])
tree.draw()
```

![](./img/42.png)

... and then simply:

```python
tree()
TypeError: < lambda > () missing 1 required keyword-only argument: 'x'

tree(x=11)
42
```