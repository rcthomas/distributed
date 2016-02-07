from __future__ import print_function, division, absolute_import

import sys

if sys.version_info[0] == 2:
    from Queue import Queue
    reload = reload
    unicode = unicode

if sys.version_info[0] == 3:
    from queue import Queue
    from importlib import reload
    unicode = str


try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch
