''' Important data structures.
'''

from collections import namedtuple

Target = namedtuple('Target', ['script', 'offset'])
def __add__(self, o):
    return Target(self.script, self.offset + o)
Target.__add__ = __add__
del __add__


class State:

    def __init__(self, rep):
        self.rep = rep

    def __repr__(self):
        return 'State.%s' % self.rep
for s in 'HALT RUN INPUT'.split():
    setattr(State, s, State(s))
del s


class Script:
    ''' A sequence of instructions and associated data.
    '''

    def __init__(self, flavor):
        self.events = {} # str -> int
        self.integers = [] # int
        self.strings = [] # str
        self.variables = [] # str
        self.targets = [] # Target
        self.builtins = [] # function

        self.flavor = flavor
        self.code = [] # instructions

    def get_event_target(self, name):
        return Target(self, self.events[name])


class ScriptContext:
    ''' Runtime stuff.
    '''

    def __init__(self, ip):
        assert isinstance(ip, Target)
        self.ip = ip
        self.state = State.RUN
        self.user = None

        self.sstack = [] # strings
        self.istack = [] # integers
        self.lstack = [] # labels
        self.ostack = [] # other objects

    def run(self, user):
        if self.state is State.HALT:
            raise Exception
        self.user = user
        self.state = State.RUN
        while self.state is State.RUN:
            assert self.ip.offset < len(self.ip.script.code)
            op, arg = self.ip.script.code[self.ip.offset]
            func = self.ip.script.flavor._funcs[op]
            self.ip += 1
            func(self, arg)
        self.user = None
