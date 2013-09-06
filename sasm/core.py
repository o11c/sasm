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

    def dump(self, out=None):
        from .parser import Kind, quote_string
        if out is None:
            out = sys.stdout
        evl = {}
        for name, offset in self.events.items():
            evl[offset] = '\non ' + name
        for script, offset in self.targets:
            if script is not self:
                continue
            if offset in evl:
                evl[offset] += '\nlabel #%d' % offset
            else:
                evl[offset] = '\nlabel #%d' % offset
        evl[0] = evl[0][1:]

        for offset, (opi, arg) in enumerate(self.code):
            if offset in evl:
                print(evl[offset], file=out)
            func = self.flavor._funcs[opi]
            name = func.__name__
            assert self.flavor._indices[name] == opi
            kind = self.flavor._kinds[name]
            if kind is Kind.LOCATION:
                lscr, loff = self.targets[arg]
                if lscr is self:
                    loc = '#%d' % loff
                else:
                    for lscrn, lscrp in self.flavor._scripts.items():
                        if lscrp is lscr:
                            break
                    else:
                        assert False, 'Bad script: %s' % lscr
                    for evn, evo in script.events.items():
                        if evo == loff:
                            loc = '%s.%s' % (lscrn, evn)
                            break
                    else:
                        assert False, 'No such event: %s' % loff
                print(name, loc, file=out)
            elif kind is Kind.INTEGER:
                print(name, self.integers[arg], file=out)
            elif kind is Kind.STRING:
                print(name, quote_string(self.strings[arg]), file=out)
            elif kind is Kind.VARIABLE:
                print(name, self.variables[arg], file=out)
            elif kind is Kind.BUILTIN:
                print(name, self.builtins[arg].__name__, file=out)
            elif kind is Kind.NONE:
                assert arg == 0
                print(name, file=out)
            else:
                assert False, 'Bad kind: %s' % kind


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
