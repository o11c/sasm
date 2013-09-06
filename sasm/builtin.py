from . import core as _core

def inputs(ctx):
    ''' s: | LINE
    '''
    ctx.state = _core.State.INPUT
    s = ctx.user.gets()
    ctx.state = _core.State.RUN
    ctx.sstack.append()

def inputi(ctx):
    ''' i: | VAL
    '''
    ctx.state = _core.State.INPUT
    i = ctx.user.geti()
    ctx.state = _core.State.RUN
    ctx.istack.append(i)

def domenu(ctx):
    ''' i: N |
        s: N*option |
        l: N*target |
        ip: one of the ls
    '''
    n = ctx.istack.pop()
    opts = ctx.sstack[-n:]
    del ctx.sstack[-n:]
    ctx.state = _core.State.INPUT
    m = ctx.user.menu(opts)
    ctx.state = _core.State.RUN
    lbls = ctx.lstack[-n:]
    del ctx.lstack[-n:]
    ctx.ip = lbls[m]

def print(ctx):
    ''' s: MSG |
    '''
    ctx.user.put(ctx.sstack.pop())
