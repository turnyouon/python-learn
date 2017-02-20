import functools

# simple decorator
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

# decorator with args
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print 'before call %s():' % func.__name__
            out = func(*args, **kw)
            print 'annotation information %s' % text
            print 'after call %s():' % func.__name__
            return out
        return wrapper
    return decorator


@log('test')
def f(log):
    print '%s' % log

f('test')