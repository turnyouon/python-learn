import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print 'before call %s():' % func.__name__
        out = func(*args, **kw)
        print 'after call %s():' % func.__name__
        return out
    return wrapper

@log
def f():
    print 'func f invoked'

f()
