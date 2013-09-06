import unittest

from sasm.user import Variables, TextUser


class TestVariables(unittest.TestCase):

    def setUp(self):
        self.v = Variables(int)

    def tearDown(self):
        del self.v

    def test_get(self):
        assert self.v['a'] == 0
        assert len(self.v) == 0
        self.v['a'] = 1
        assert self.v['a'] == 1
        assert len(self.v) == 1

    def test_set(self):
        assert len(self.v) == 0
        self.v['a'] = 0
        assert len(self.v) == 0
        del self.v['a']
        assert len(self.v) == 0
        self.v['a'] = 1
        assert len(self.v) == 1
        self.v['a'] = 0
        assert len(self.v) == 0
        self.v['a'] = 1
        assert len(self.v) == 1
        del self.v['a']
        assert len(self.v) == 0


class TestTextUser(unittest.TestCase):

    def test_vars(self):
        u = TextUser(None, None)
        assert u.loads('str') == ''
        u.stores('str', 'val')
        assert u.loads('str') == 'val'
        assert u.loadi('int') == 0
        u.storei('int', 42)
        assert u.loadi('int') == 42

    def test_io(self):
        from io import StringIO
        input = StringIO('String!\n42\n')
        output = StringIO()
        u = TextUser(input, output)
        u.put('Hello, World!')
        assert u.gets() == 'String!'
        assert u.geti() == 42
        assert output.getvalue() == 'Hello, World!\n'

    def test_menu(self):
        from io import StringIO
        input = StringIO('1\n0\n')
        output = StringIO()
        u = TextUser(input, output)
        assert u.menu(['hello', 'world']) == 1
        assert u.menu(['goodbye', 'world']) == 0
        assert output.getvalue() == '0. hello\n1. world\n0. goodbye\n1. world\n'
