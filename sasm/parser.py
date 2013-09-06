''' Responsible for turning an ASM file into a sequence of asm instructions.
'''

import types

from .core import Target


class LameParser:

    def __init__(self, input):
        self._input = iter(input)

    def __iter__(self):
        return self

    def __next__(self):
        line = ''
        while line == '':
            line = next(self._input).strip()
        if ' ' in line:
            return line.split(' ', 1)
        else:
            return line, None


class Kind:

    def __init__(self, rep):
        self.rep = rep

    def __repr__(self):
        return 'Kind.%s' % self.rep
for s in 'COMMENT ENTRY LABEL NONE LOCATION INTEGER STRING VARIABLE BUILTIN'.split():
    setattr(Kind, s, Kind(s))
del s


class Flavor:

    def __init__(self):
        self._kinds = {} # str -> Kind
        self._indices = {} # str -> int
        self._funcs = [] # int -> func
        self._builtins = {} # str -> func
        self._scripts = {} # str -> script

    def builtin(self, name, func):
        assert name not in self._builtins
        self._builtins[name] = func

    def op_comment(self, name):
        assert name not in self._kinds
        self._kinds[name] = Kind.COMMENT

    def op_entry(self, name):
        assert name not in self._kinds
        self._kinds[name] = Kind.ENTRY

    def op_label(self, name):
        assert name not in self._kinds
        self._kinds[name] = Kind.LABEL

    def _op(self, kind, name, func):
        assert name not in self._kinds
        self._kinds[name] = kind
        self._indices[name] = len(self._funcs)
        self._funcs.append(func)

    def op_n(self, name, func):
        self._op(Kind.NONE, name, func)

    def op_l(self, name, func):
        self._op(Kind.LOCATION, name, func)

    def op_i(self, name, func):
        self._op(Kind.INTEGER, name, func)

    def op_s(self, name, func):
        self._op(Kind.STRING, name, func)

    def op_v(self, name, func):
        self._op(Kind.VARIABLE, name, func)

    def op_b(self, name, func):
        self._op(Kind.BUILTIN, name, func)

    def parse_code(self, name, input):
        from .core import Script
        script = Script(self)
        self._scripts[name] = script

        integers = {} # int -> index into script.integers
        strings = {} # str -> index into script.strings
        variables = {} # str -> index into script.variables
        builtins = {} # function -> index into script.builtins
        remote_targets = {} # Target -> index into script.targets
        local_targets = {} # str -> int index into script.targets
        labels = {} # str -> code offset for this label name

        for cmd, rarg in LameParser(input):
            kind = self._kinds[cmd]
            if kind is Kind.COMMENT:
                continue
            if kind is Kind.ENTRY:
                assert rarg
                assert ' ' not in rarg
                assert '.' not in rarg
                assert rarg not in script.events
                script.events[rarg] = len(script.code)
            if kind is Kind.LABEL:
                assert rarg
                assert ' ' not in rarg
                assert '.' not in rarg
                assert rarg not in labels
                labels[rarg] = len(script.code)
            if kind is Kind.LOCATION:
                assert rarg
                assert ' ' not in rarg
                lst = len(script.targets)
                # label if local, or event if remote
                if '.' in rarg:
                    # remote event targets are always already known
                    tsn, tse = rarg.split('.')
                    ts = self._scripts[tsn]
                    target = Target(ts, ts.events[tse])
                    larg = remote_targets.setdefault(target, lst)
                    if larg == lst:
                        script.targets.append(target)
                else:
                    larg = local_targets.setdefault(rarg, lst)
                    if larg == lst:
                        script.targets.append(Target(None, None))
                script.code.append((self._indices[cmd], larg))
            if kind is Kind.INTEGER:
                assert rarg
                iv = int(rarg)
                lsi = len(script.integers)
                iarg = integers.setdefault(iv, lsi)
                if iarg == lsi:
                    script.integers.append(iv)
                script.code.append((self._indices[cmd], iarg))
            if kind is Kind.STRING:
                assert rarg
                lss = len(script.strings)
                rarg = parse_string(rarg)
                sarg = strings.setdefault(rarg, lss)
                if sarg == lss:
                    script.strings.append(rarg)
                script.code.append((self._indices[cmd], sarg))
            if kind is Kind.VARIABLE:
                assert rarg
                assert ' ' not in rarg
                lsv = len(script.variables)
                varg = variables.setdefault(rarg, lsv)
                if varg == lsv:
                    script.variables.append(rarg)
                script.code.append((self._indices[cmd], varg))
            if kind is Kind.BUILTIN:
                assert rarg
                assert ' ' not in rarg
                bv = self._builtins[rarg]
                lsb = len(script.builtins)
                barg = builtins.setdefault(bv, lsb)
                if barg == lsb:
                    script.builtins.append(bv)
                script.code.append((self._indices[cmd], barg))
            if kind is Kind.NONE:
                assert rarg is None
                script.code.append((self._indices[cmd], 0))
        for lname, sto in local_targets.items():
            loff = labels[lname]
            script.targets[sto] = Target(script, loff)
        return script

def parse_string(raw):
    assert raw.startswith('"')
    l = len(raw) - 1
    assert l >= 1
    assert raw.endswith('"')
    if '\\' not in raw:
        return raw[1:-1]
    out = ''
    i = 1
    while i < l:
        c = raw[i]
        if c == '\\':
            i += 1
            assert i < l
            c = raw[i]
            if c == 'a':
                c = '\a'
            elif c == 'b':
                c = '\b'
            elif c == 'e':
                c = '\x1b'
            elif c == 'f':
                c = '\f'
            elif c == 'n':
                c = '\n'
            elif c == 'r':
                c = '\r'
            elif c == 't':
                c = '\t'
            elif c == 'v':
                c = '\v'
            elif c == 'x':
                i += 1
                assert i < l
                c = raw[i]
                i += 1
                assert i < l
                c = chr(int(c + raw[i], 16))
            else:
                assert 'Unknown escape: ' + c
        out.append(c)
        continue

def quote_string(cooked):
    return '"%s"' % cooked.replace('\\', '\\\\').replace('"', '\\"')
