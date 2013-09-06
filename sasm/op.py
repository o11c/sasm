from . import core as _core

def pushi(ctx, ii):
    ''' i: | LIT
    '''
    ctx.istack.append(ctx.ip.script.integers[ii])

def pushs(ctx, si):
    ''' s: | LIT
    '''
    ctx.sstack.append(ctx.ip.script.strings[si])

def pushl(ctx, li):
    ''' l: | LIT
    '''
    ctx.lstack.append(ctx.ip.script.targets[li])

def popi(ctx, _):
    ''' i: BLAH |
    '''
    ctx.istack.pop()

def pops(ctx, _):
    ''' s: BLAH |
    '''
    ctx.sstack.pop()

def popl(ctx, _):
    ''' l: BLAH |
    '''
    ctx.lstack.pop()

def popo(ctx, _):
    ''' o: BLAH |
    '''
    ctx.ostack.pop()

def dupi(ctx, _):
    ''' i: V | V V
    '''
    ctx.istack.append(ctx.istack[-1])

def dups(ctx, _):
    ''' s: V | V V
    '''
    ctx.sstack.append(ctx.sstack[-1])

def dupl(ctx, _):
    ''' l: V | V V
    '''
    ctx.lstack.append(ctx.lstack[-1])

def dupo(ctx, _):
    ''' o: V | V V
    '''
    ctx.ostack.append(ctx.ostack[-1])


def end(ctx, _):
    ''' state: end
    '''
    ctx.state = _core.State.HALT

def call(ctx, li):
    ''' l: | ip
        ip: LIT
    '''
    ctx.lstack.append(ctx.ip)
    ctx.ip = ctx.ip.script.targets[li]

def ret(ctx, _):
    ''' l: R |
        ip: R
    '''
    ctx.ip = ctx.lstack.pop()

def builtin(ctx, bi):
    ''' arbitrary
    '''
    ctx.ip.script.builtins[bi](ctx)

def loads(ctx, vi):
    ''' v: NAME |
        s: | VAL
    '''
    vi = ctx.vstack.pop()
    v = ctx.ip.script.variables[vi]
    s = ctx.user.loads(v)
    ctx.sstack.append(s)

def stores(ctx, vi):
    ''' v: NAME |
        s: VAL |
    '''
    vi = ctx.vstack.pop()
    v = ctx.ip.script.variables[vi]
    s = ctx.sstack.pop()
    ctx.user.stores(v, s)

def loadi(ctx, vi):
    ''' v: NAME |
        s: | VAL
    '''
    vi = ctx.vstack.pop()
    v = ctx.ip.script.variables[vi]
    i = ctx.user.loadi(v)
    ctx.istack.append(i)

def storei(ctx, vi):
    ''' v: NAME |
        s: VAL |
    '''
    vi = ctx.vstack.pop()
    v = ctx.ip.script.variables[vi]
    i = ctx.istack.pop()
    ctx.user.storei(v, i)
