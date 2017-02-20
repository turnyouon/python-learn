

class AutoConnect(object):
    conn = 'auto connect'

    print 'log %s' % conn

    def __init__(self, func):
        self.func = func
        self.exception = None

    def __call__(self, *args, **kwargs):
        return self.func(AutoConnect.conn)

@AutoConnect
def do_something(conn):
    print 'do_something invoked'
    return 1

retval = do_something()

print retval

@AutoConnect
def do_other_thing(conn):
    def log():
        print conn + ' in do other thing'

    log()

do_other_thing()
