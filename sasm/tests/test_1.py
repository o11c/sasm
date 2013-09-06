from io import StringIO
import os
import sys
import unittest

import sasm.core, sasm.parser, sasm.builtin, sasm.op, sasm.user

class Test1(unittest.TestCase):

    def setUp(self):
        flavor = sasm.parser.Flavor()
        flavor.op_comment('#')
        flavor.op_comment('//')
        flavor.op_entry('on')
        flavor.op_label('label')

        flavor.builtin('print', sasm.builtin.print)
        flavor.builtin('inputs', sasm.builtin.inputs)
        flavor.builtin('inputi', sasm.builtin.inputi)
        flavor.builtin('domenu', sasm.builtin.domenu)

        flavor.op_i('pushi', sasm.op.pushi)
        flavor.op_s('pushs', sasm.op.pushs)
        flavor.op_l('pushl', sasm.op.pushl)
        flavor.op_n('popi', sasm.op.popi)
        flavor.op_n('pops', sasm.op.pops)
        flavor.op_n('popl', sasm.op.popl)
        flavor.op_n('popo', sasm.op.popo)
        flavor.op_n('dupi', sasm.op.dupi)
        flavor.op_n('dups', sasm.op.dups)
        flavor.op_n('dupl', sasm.op.dupl)
        flavor.op_n('dupo', sasm.op.dupo)
        flavor.op_n('end', sasm.op.end)
        flavor.op_l('call', sasm.op.call)
        flavor.op_n('ret', sasm.op.ret)
        flavor.op_b('builtin', sasm.op.builtin)
        flavor.op_v('loads', sasm.op.loads)
        flavor.op_v('stores', sasm.op.stores)
        flavor.op_v('loadi', sasm.op.loadi)
        flavor.op_v('storei', sasm.op.storei)

        fn = os.path.join(os.path.dirname(__file__), '1.sasm')
        self.script = flavor.parse_code('test1', open(fn))

    def tearDown(self):
        del self.script

    def test_1a(self):
        input = None
        output = StringIO()
        user = sasm.user.TextUser(input, output)
        ctx = sasm.core.ScriptContext(self.script.get_event_target('init'))
        ctx.run(user)
        assert output.getvalue() == 'script is starting ...\nOkay!\n'

    def test_1b0(self):
        input = StringIO('0\n')
        output = StringIO()
        user = sasm.user.TextUser(input, output)
        ctx = sasm.core.ScriptContext(self.script.get_event_target('click'))
        ctx.run(user)
        assert output.getvalue() == '0. hello\n1. world\nyou said hi\n'

    def test_1b1(self):
        input = StringIO('1\n')
        output = StringIO()
        user = sasm.user.TextUser(input, output)
        ctx = sasm.core.ScriptContext(self.script.get_event_target('click'))
        ctx.run(user)
        assert output.getvalue() == '0. hello\n1. world\nyou said earth\n'

    def test_dump(self):
        fn = os.path.join(os.path.dirname(__file__), '1.raw')
        dump = open(fn).read()
        out = StringIO()
        self.script.dump(out)
        assert out.getvalue() == dump
