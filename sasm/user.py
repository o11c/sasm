''' Mockup of player data.
'''

class Variables:
    ''' Default-eliminating container for variables.
    '''

    def __init__(self, type):
        self._type = type
        self._default = type()
        self._impl = {}

    def __getitem__(self, idx):
        return self._impl.get(idx, self._default)

    def __setitem__(self, idx, val):
        assert isinstance(val, self._type)
        if val != self._default:
            self._impl[idx] = val
            return
        if idx in self._impl:
            del self._impl[idx]

    def __delitem__(self, idx):
        self[idx] = self._default

    def __len__(self):
        return len(self._impl)


class TextUser:
    ''' A user who is connected via files.
    '''
    def __init__(self, input, output):
        self._input = input
        self._output = output
        self._vars = Variables(str)
        self._vari = Variables(int)

    def stores(self, key, val):
        self._vars[key] = val

    def loads(self, key):
        return self._vars[key]

    def storei(self, key, val):
        self._vari[key] = val

    def loadi(self, key):
        return self._vari[key]

    def put(self, line):
        print(line, file=self._output)

    def geti(self):
        return int(self.gets())

    def gets(self):
        l = self._input.readline()
        assert l.endswith('\n')
        return l[:-1]

    def menu(self, opts):
        for i, line in enumerate(opts):
            self.put('%d. %s' % (i, line))
        i = self.geti()
        assert 0 <= i < len(opts)
        return i

    def assert_end(self):
        assert self._input.readline() == ''
