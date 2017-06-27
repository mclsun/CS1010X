from functools import wraps
import sys
import time

## Profiling function

def profile_fn(fn, times):
    start = time.clock()
    for i in range(times):
        fn()
    end = time.clock()
    return (end - start)*1000

## Tracing functions

original_fn = {}

def replace_fn(fn_src, fn_dest):
    mod = sys.modules[fn_src.__module__]
    setattr(mod, fn_src.__name__, fn_dest)

def trace(fn):
    global original_fn

    key = fn.__module__ + fn.__name__
    if key in original_fn:
        return

    original_fn[key] = fn
    replace_fn(fn, TraceCalls()(fn))

def untrace(fn):
    global original_fn
    key = fn.__module__ + fn.__name__
    if key in original_fn:
        replace_fn(fn, original_fn[key])
        del original_fn[key]

# http://eli.thegreenplace.net/2012/08/22/easy-tracing-of-nested-function-calls-in-python/
class TraceCalls(object):
    """ Use as a decorator on functions that should be traced. Several
        functions can be decorated - they will all be indented according
        to their call depth.
    """
    def __init__(self, stream=sys.stdout, indent_step=2, show_ret=True):
        self.stream = stream
        self.indent_step = indent_step
        self.show_ret = show_ret

        # This is a class attribute since we want to share the indentation
        # level between different traced functions, in case they call
        # each other.
        TraceCalls.cur_indent = 0

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            indent = ' ' * TraceCalls.cur_indent
            argstr = ', '.join(
                [repr(a) for a in args] +
                ["%s=%s" % (a, repr(b)) for a, b in kwargs.items()])
            self.stream.write('%s%s(%s)\n' % (indent, fn.__name__, argstr))

            TraceCalls.cur_indent += self.indent_step
            ret = fn(*args, **kwargs)
            TraceCalls.cur_indent -= self.indent_step

            if self.show_ret:
                self.stream.write('%s--> %s\n' % (indent, ret))
            return ret
        return wrapper