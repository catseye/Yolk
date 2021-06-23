#!/usr/bin/env python


class Sexpr(object):
    def is_atom(self, s):
       return False


class Atom(Sexpr):
    def __init__(self, s):
       assert s in ('ifeq', 'quote', 'arg', 'head', 'tail', 'self', 'cons'), s
       self.s = s

    def __str__(self):
       return self.s

    def is_atom(self, s):
       return self.s == s

    def __eq__(self, other):
       return isinstance(other, Atom) and other.s == self.s


class List(Sexpr):
    def __init__(self, sexprs):
       for s in sexprs:
           assert isinstance(s, Sexpr)
       self.sexprs = sexprs

    def __str__(self):
       return "(%s)" % ' '.join([s.__str__() for s in self.sexprs])

    def head(self):
       return self.sexprs[0]

    def tail(self):
       return List(self.sexprs[1:])

    def __eq__(self, other):
       return isinstance(other, List) and other.sexprs == self.sexprs


class Scanner(object):
    def __init__(self, s):
        self.s = s

    def scan(self):
        while self.s and self.s[0].isspace():
            self.s = self.s[1:]

        if not self.s:
            return None

        if self.s[0] in ('(', ')'):
            token = self.s[0]
            self.s = self.s[1:]
            return token

        if self.s[0].isalpha():
            token = ''
            while self.s and self.s[0].isalpha():
                token += self.s[0]
                self.s = self.s[1:]
            return token

        raise ValueError('illegal character: ' + self.s[0])


class Parser(object):

    def __init__(self, s):
        self.scanner = Scanner(s)

    def sexpr(self):
        token = self.scanner.scan()
        if token == ')':
            return None
        if token == '(':
            l = []
            sub = self.sexpr()
            while sub is not None:
                l.append(sub)
                sub = self.sexpr()
            return List(l)
        else:
            return Atom(token)


def cons(a, b):
    return List([a] + b.sexprs)


def eval_yolk(full, prog, arg):
    if prog.is_atom('arg'):
        return arg
    if prog.head().is_atom('head'):
        return eval_yolk(full, prog.tail().head(), arg).head()
    if prog.head().is_atom('tail'):
        return eval_yolk(full, prog.tail().head(), arg).tail()
    if prog.head().is_atom('cons'):
        return cons(eval_yolk(full, prog.tail().head(), arg), eval_yolk(full, prog.tail().tail().head(), arg))
    if prog.head().is_atom('quote'):
        return prog.tail().head()
    if prog.head().is_atom('ifeq'):
        if eval_yolk(full, prog.tail().head(), arg) == eval_yolk(full, prog.tail().tail().head(), arg):
            return eval_yolk(full, prog.tail().tail().tail().head(), arg)
        else:
            return eval_yolk(full, prog.tail().tail().tail().tail().head(), arg)
    if prog.head().is_atom('self'):
        return eval_yolk(full, full, eval_yolk(full, prog.tail().head(), arg))
    raise ValueError("Cannot evaluate %r" % prog)


def run(ptext, atext):
    p = Parser(ptext).sexpr()
    a = Parser(atext).sexpr()
    r = eval_yolk(p, p, a)
    return r


def main():
    import sys
    with open(sys.argv[1], 'r') as f:
        prog = f.read()
    if len(sys.argv) >= 4 and sys.argv[2] == '-i':
        with open(sys.argv[3], 'r') as f:
            inp = f.read()
    else:
        inp = sys.stdin.read()
    if not inp:
        inp = 'ifeq'
    result = run(prog, inp)
    print(result)


def target(*args):
    import os
    
    def rpython_load(filename):
        fd = os.open(filename, os.O_RDONLY, 0o644)
        text = ''
        chunk = os.read(fd, 1024)
        text += chunk
        while len(chunk) == 1024:
            chunk = os.read(fd, 1024)
            text += chunk
        os.close(fd)
        return text

    def rpython_input():
        accum = ''
        done = False
        while not done:
            s = os.read(1, 1)
            if not s:
                done = True
            accum += s
        return accum

    def rpython_main(argv):
        program = rpython_load(argv[1])
        if len(argv) >= 4 and argv[2] == '-i':
            inp = rpython_load(argv[3])
        else:
            inp = rpython_input()
        if not inp:
            inp = 'ifeq'
        result = run(program, inp)
        print(result.__str__())
        return 0

    return rpython_main, None


if __name__ == '__main__':
    main()
