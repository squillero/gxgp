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

### Copyright

**Copyright © 2024 by [Giovanni Squillero](https://squillero.github.io/) <[giovanni.squillero@polito.it](mailto:giovanni.squillero@polito.it)**>  
Distributed under [*Zero-Clause BSD*](https://www.tldrlegal.com/license/bsd-0-clause-license) (SPDX-License-Identifier: `0BSD`).
