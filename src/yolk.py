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
       return "(%s)" % ' '.join([str(s) for s in self.sexprs])

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


def eval(full, prog, arg):
    if prog.is_atom('arg'):
        return arg
    if prog.head().is_atom('head'):
        return eval(full, prog.tail().head(), arg).head()
    if prog.head().is_atom('tail'):
        return eval(full, prog.tail().head(), arg).tail()
    if prog.head().is_atom('cons'):
        return cons(eval(full, prog.tail().head(), arg), eval(full, prog.tail().tail().head(), arg))
    if prog.head().is_atom('quote'):
        return prog.tail().head()
    if prog.head().is_atom('ifeq'):
        if eval(full, prog.tail().head(), arg) == eval(full, prog.tail().tail().head(), arg):
            return eval(full, prog.tail().tail().tail().head(), arg)
        else:
            return eval(full, prog.tail().tail().tail().tail().head(), arg)
    if prog.head().is_atom('self'):
        return eval(full, full, eval(full, prog.tail().head(), arg))
    return Atom('head').head()


def run(ptext, atext):
    p = Parser(ptext).sexpr()
    return eval(p, p, Parser(atext).sexpr())


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        inp = sys.stdin.read()
        if not inp:
            inp = 'ifeq'
        result = run(f.read(), inp)
        print result
