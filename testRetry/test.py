import time
import subprocess
import functools


class ShellError(Exception):
    '''shell error'''


class ShellCmd(object):
    '''
    classdocs
    '''

    def __init__(self, cmd, workdir=None, pipe=True):
        '''
        Constructor
        '''
        self.cmd = cmd
        if pipe:
            self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                            stderr=subprocess.PIPE, close_fds=True, executable='/bin/bash', cwd=workdir)
        else:
            self.process = subprocess.Popen(cmd, shell=True, executable='/bin/bash', cwd=workdir)

        self.stdout = None
        self.stderr = None
        self.return_code = None

    def raise_error(self):
        err = []
        err.append('failed to execute shell command: %s' % self.cmd)
        err.append('return code: %s' % self.process.returncode)
        err.append('stdout: %s' % self.stdout)
        err.append('stderr: %s' % self.stderr)
        raise ShellError('\n'.join(err))

    def __call__(self, is_exception=True):
        (self.stdout, self.stderr) = self.process.communicate()
        if is_exception and self.process.returncode != 0:
            self.raise_error()

        self.return_code = self.process.returncode
        self.return_code = -11
        return self.stdout


def call(cmd, exception=True, workdir=None):
    return ShellCmd(cmd, workdir)(exception)


def run(cmd, workdir=None):
    s = ShellCmd(cmd, workdir)
    s(False)
    return s.return_code

def retry(times=3, sleep_time=3):
    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            for i in range(0, times):
                print "OK"
                try:
                    return f(*args, **kwargs)
                except:
                    time.sleep(sleep_time)
            raise

        return inner
    return wrap

@retry(times=3, sleep_time=3)
def print_info():
    cmd = ShellCmd("ls -l")
    out = cmd(False)
    if cmd.return_code == -11:
        raise
    elif cmd.return_code != 0:
        return None


print_info()