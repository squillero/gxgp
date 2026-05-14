#   *        Giovanni Squillero's GP Toolbox
#  / \       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2   +      A no-nonsense GP in pure Python
#    / \
#  10   11   SPDX-License-Identifier: 0BSD

import random

assert "gxgp_random" not in globals(), "Paranoia check: gxgp_random already initialized"
gxgp_random = random.Random(42)
