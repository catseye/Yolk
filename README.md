Yolk
====

Yolk is a programming language (or computational calculus) with a very
small meta-circular definition.

A Yolk program consists of an S-expression.  This gives the body of a
function which takes an S-expression as its argument and which evaluates to
an S-expression.

In this context, an S-expression is an atom or a list of S-expressions.

An atom is one of the following seven atomic symbols:
`ifeq`, `quote`, `head`, `tail`, `cons`, `arg`, or `self`.

Basic Semantics
---------------

    -> Tests for functionality "Evaluate Yolk program"

`(quote A)` evaluates to A.  (It does not evaluate A.)

    | (quote cons)
    = cons

    | (quote (cons (head cons tail) cons))
    = (cons (head cons tail) cons)

`(head A)` evaluates A to a list and itself evaluates to first element of the
list.

    | (head (quote (cons tail tail)))
    = cons

If A is not a list, `(head A)`, crashes.

    | (head (quote head))
    ? 

`(tail A)` evaluates A to a list and itself evaluates to everything except the
first element of the list.

    | (tail (quote (cons head head)))
    = (head head)

If A is not a list, `(tail A)` crashes.

    | (tail (quote tail))
    ? 

`(cons A B)` evaluates A to a S-expression and B to a list, and evaluates to a list
which is the same as B except it has an extra element on the front, B.

    | (cons (quote quote) (quote (head tail cons)))
    = (quote head tail cons)

`(ifeq A B C D)` evaluates A and B; if they evaluate to the same atom
then this form evaluates to what C evaluates to, otherwise it evaluates to
what D evaluates to.

    | (ifeq (quote head) (quote head) (quote cons) (quote self))
    = cons

    | (ifeq (quote head) (quote tail) (quote cons) (quote self))
    = self

Advanced semantics
------------------

`arg` evaluates to the argument of the current program-function.

    | arg
    + ifeq
    = ifeq

    | (tail arg)
    + (ifeq ifeq (ifeq ifeq))
    = (ifeq (ifeq ifeq))

`(self A)` evaluates A to an S-expression, then evaluates the main
program-function with that as the argument, and evaluates to the result
of that.

    | (ifeq (head arg) (quote cons) arg (self (tail arg)))
    + (head head cons tail tail)
    = (cons tail tail)

Meta-circular Interpreter
-------------------------

### Preliminary Sketch ###

I believe it is possible to write a meta-circular interpreter for Yolk.

We'll start with a sketch of it, which is not a full interpreter but which
gets the basic idea across.  The sketch looks like this:

    (ifeq arg (quote arg)
        arg
        (ifeq (head arg) (quote head)
            (head (self (head (tail arg))))
            (ifeq (head arg) (quote tail)
                (tail (self (head (tail arg))))
                (ifeq (head arg) (quote cons)
                    (cons (self (head (tail arg))) (self (head (tail (tail arg)))))
                    (ifeq (head arg) (quote quote)
                        (head (tail arg))
                        (ifeq (head arg) (quote ifeq)
                            (ifeq (self (head (tail arg)))
                                (self (head (tail (tail arg))))
                                (self (head (tail (tail (tail arg)))))
                                (self (head (tail (tail (tail (tail arg)))))))
                            (ifeq (head arg) (quote self)
                                (self (self (head (tail arg))))
                                (ifeq))))))))

The `(ifeq)` at the end there is just there to trigger a runtime error if
things go badly.

We test this meta-circular interpreter on the previous illustrations of the
basic semantics as follows.  The interpreter itself is sourced from a file to
reduce repetition in this document.

    -> Tests for functionality "Evaluate Yolk program with MCI Sketch"

    -> Functionality "Evaluate Yolk program with MCI Sketch" is implemented by
    -> shell command "src/yolk.py eg/mci-sketch.yolk <%(test-body-file)"

    | (quote cons)
    = cons

    | (quote (cons (head cons tail) cons))
    = (cons (head cons tail) cons)

    | (head (quote (cons tail tail)))
    = cons

    | (head (quote head))
    ? 

    | (tail (quote (cons head head)))
    = (head head)

    | (tail (quote tail))
    ? 

    | (cons (quote quote) (quote (head tail cons)))
    = (quote head tail cons)

    | (ifeq (quote head) (quote head) (quote cons) (quote self))
    = cons

    | (ifeq (quote head) (quote tail) (quote cons) (quote self))
    = self

### With Input ###

    -> Tests for functionality "Evaluate Yolk program with MCI with arg"

    -> Functionality "Evaluate Yolk program with MCI with arg" is implemented by
    -> shell command "src/yolk.py eg/mci-with-arg.yolk <%(test-body-file)"

However, there is a small problem.  Where does this interpreter get its
input from, for `arg`?

Instead of having the input to the MCI just be the program to be interpreted,
it must be extended: a 2-element list where the first element is the program
and the second is the input.

In our first step towards doing this, we will just package the program and
its input into this list, but still ignore the input.  We change the MCI to
handle this format by

*   replacing `arg`, where we read it, with `(head arg)`, and
*   replacing `arg`, where we evaluate to it, with `(head (tail arg))`, and
*   replacing the modified `arg`, where we pass it to `self`,
    e.g. `(self (head (tail arg)))`, with
    `(cons (head (tail (head arg))) (tail arg))`

And we get:

    (ifeq (head arg) (quote arg)
        (head (tail arg))
        (ifeq (head (head arg)) (quote head)
            (head (self (cons (head (tail (head arg))) (tail arg))))
            (ifeq (head (head arg)) (quote tail)
                (tail (self (cons (head (tail (head arg))) (tail arg))))
                (ifeq (head (head arg)) (quote cons)
                    (cons (self (cons (head (tail (head arg))) (tail arg))) (self (cons (head (tail (tail (head arg)))) (tail arg))))
                    (ifeq (head (head arg)) (quote quote)
                        (head (tail (head arg)))
                        (ifeq (head (head arg)) (quote ifeq)
                            (ifeq (self (cons (head (tail (head arg))) (tail arg)))
                                  (self (cons (head (tail (tail (head arg)))) (tail arg)))
                                  (self (cons (head (tail (tail (tail (head arg))))) (tail arg)))
                                  (self (cons (head (tail (tail (tail (tail (head arg)))))) (tail arg))))
                            (ifeq (head (head arg)) (quote self)
                                (self (self (head (tail arg))))
                                (ifeq))))))))

Now we test it.

`quote` in MCI.

    | ((quote ifeq) cons)
    = ifeq

    | ((quote (ifeq (head ifeq tail) ifeq)) cons)
    = (ifeq (head ifeq tail) ifeq)

`head` in MCI.
 
    | ((head (quote (ifeq tail tail))) cons)
    = ifeq

`tail` in MCI.

    | ((tail (quote (cons head head))) cons)
    = (head head)
 
`cons` in MCI.
 
    | ((cons (quote quote) (quote (head tail ifeq))) ifeq)
    = (quote head tail ifeq)

`ifeq` in MCI.

    | ((ifeq (quote head) (quote head) (quote cons) (quote self)) ifeq)
    = cons

    | ((ifeq (quote head) (quote tail) (quote cons) (quote self)) ifeq)
    = self

`arg` in MCI.

    | (arg ifeq)
    = ifeq

    | ((tail arg) (ifeq ifeq (ifeq ifeq)))
    = (ifeq (ifeq ifeq))

### With Recursion ###

    -> Tests for functionality "Evaluate Yolk program"

Now the final stroke — fix the implementation of `self`.  This is kind of
tricky.

In the MCI, `self` is used for recursively interpreting parts of the "target
program", i.e. the program given in the head of the arg.

In the program being interpreted, `self` is used for recursing *that* program.

So, we evaluate the first argument to a value:
    
    (self (cons (head (tail (head arg))) (tail arg)))

Then we want to evaluate the target program, all of it, on that value.

But wait!

We don't have a way to evaluate the entire target program!  We don't even *have*
the entire target program!  We'll have to keep a copy around, so instead of a
2-element list, we'll need a 3-element list (I knew that.)

    | (ifeq (head arg) (quote arg)
    |     (head (tail (tail arg)))
    |     (ifeq (head (head arg)) (quote head)
    |         (head (self (cons (head (tail (head arg))) (tail arg))))
    |         (ifeq (head (head arg)) (quote tail)
    |             (tail (self (cons (head (tail (head arg))) (tail arg))))
    |             (ifeq (head (head arg)) (quote cons)
    |                 (cons (self (cons (head (tail (head arg))) (tail arg))) (self (cons (head (tail (tail (head arg)))) (tail arg))))
    |                 (ifeq (head (head arg)) (quote quote)
    |                     (head (tail (head arg)))
    |                     (ifeq (head (head arg)) (quote ifeq)
    |                         (ifeq (self (cons (head (tail (head arg))) (tail arg)))
    |                               (self (cons (head (tail (tail (head arg)))) (tail arg)))
    |                               (self (cons (head (tail (tail (tail (head arg))))) (tail arg)))
    |                               (self (cons (head (tail (tail (tail (tail (head arg)))))) (tail arg))))
    |                         (ifeq (head (head arg)) (quote self)
    |                             (self (self (head (tail arg))))
    |                             (ifeq))))))))
    + (
    +   (ifeq arg (quote tail) (quote cons) (quote self))
    +   (ifeq arg (quote tail) (quote cons) (quote self))
    +   tail
    + )
    = cons

    | (ifeq (head arg) (quote arg)
    |     (head (tail (tail arg)))
    |     (ifeq (head (head arg)) (quote head)
    |         (head (self (cons (head (tail (head arg))) (tail arg))))
    |         (ifeq (head (head arg)) (quote tail)
    |             (tail (self (cons (head (tail (head arg))) (tail arg))))
    |             (ifeq (head (head arg)) (quote cons)
    |                 (cons (self (cons (head (tail (head arg))) (tail arg))) (self (cons (head (tail (tail (head arg)))) (tail arg))))
    |                 (ifeq (head (head arg)) (quote quote)
    |                     (head (tail (head arg)))
    |                     (ifeq (head (head arg)) (quote ifeq)
    |                         (ifeq (self (cons (head (tail (head arg))) (tail arg)))
    |                               (self (cons (head (tail (tail (head arg)))) (tail arg)))
    |                               (self (cons (head (tail (tail (tail (head arg))))) (tail arg)))
    |                               (self (cons (head (tail (tail (tail (tail (head arg)))))) (tail arg))))
    |                         (ifeq (head (head arg)) (quote self)
    |                             (self (self (head (tail arg))))
    |                             (ifeq))))))))
    + (
    +   (ifeq arg (quote tail) (quote cons) (quote self))
    +   (ifeq arg (quote tail) (quote cons) (quote self))
    +   head
    + )
    = self

We'll also need some way to evaluate that entire client program.  Well, we have ourselves,
the MCI, so that should be OK.   ...right?  Let's try again.

We evaluate the first argument to a value:

    let val = (self (cons (head (tail (head arg))) (tail arg)))

Then we get the target program:

    let pgm = (head (tail arg))

Then we evaluate the target program, all of it, on that value.

    (self (list pgm pgm val))

Of course we don't have `list` so we say

    (self (cons pgm (cons pgm (cons val ()))))

Nor do we have `()` so

    (self (cons pgm (cons pgm (cons val (tail (quote (tail)))))))

Nor do we have `let` so

    (self (cons (head (tail arg))
            (cons (head (tail arg))
              (cons (self (cons (head (tail (head arg))) (tail arg))) (tail (quote (tail)))))))

And we hold our breath and:

    | (ifeq (head arg) (quote arg)
    |     (head (tail (tail arg)))
    |     (ifeq (head (head arg)) (quote head)
    |         (head (self (cons (head (tail (head arg))) (tail arg))))
    |         (ifeq (head (head arg)) (quote tail)
    |             (tail (self (cons (head (tail (head arg))) (tail arg))))
    |             (ifeq (head (head arg)) (quote cons)
    |                 (cons (self (cons (head (tail (head arg))) (tail arg))) (self (cons (head (tail (tail (head arg)))) (tail arg))))
    |                 (ifeq (head (head arg)) (quote quote)
    |                     (head (tail (head arg)))
    |                     (ifeq (head (head arg)) (quote ifeq)
    |                         (ifeq (self (cons (head (tail (head arg))) (tail arg)))
    |                               (self (cons (head (tail (tail (head arg)))) (tail arg)))
    |                               (self (cons (head (tail (tail (tail (head arg))))) (tail arg)))
    |                               (self (cons (head (tail (tail (tail (tail (head arg)))))) (tail arg))))
    |                         (ifeq (head (head arg)) (quote self)
    |                             (self (cons (head (tail arg))
    |                                     (cons (head (tail arg))
    |                                       (cons (self (cons (head (tail (head arg))) (tail arg))) (tail (quote (tail)))))))
    |                             (ifeq))))))))
    + (
    +   (ifeq (head arg) (quote ifeq) arg (self (tail arg)))
    +   (ifeq (head arg) (quote ifeq) arg (self (tail arg)))
    +   (head head ifeq tail tail)
    + )
    = (ifeq tail tail)

Huzzah!  Now we test all the things again...

    -> Tests for functionality "Evaluate Yolk program with MCI"

    -> Functionality "Evaluate Yolk program with MCI" is implemented by
    -> shell command "src/yolk.py eg/yolk.yolk <%(test-body-file)"

`(quote A)` evaluates to A.  (It does not evaluate A.)

    | ((quote ifeq) (quote ifeq) cons)
    = ifeq

    | ((quote (cons (head cons tail) cons)) (quote (cons (head cons tail) cons)) ifeq)
    = (cons (head cons tail) cons)

`(head A)` evaluates A to a list and itself evaluates to first element of the
list.

    | ((head (quote (cons tail tail))) (head (quote (cons tail tail))) ifeq)
    = cons

If A is not a list, `(head A)` crashes.

    | ((head (quote head)) (head (quote head)) cons)
    ? 

`(tail A)` evaluates A to a list and itself evaluates to everything except the
first element of the list.

    | ((tail (quote (cons head head))) (tail (quote (cons head head))) ifeq)
    = (head head)

If A is not a list, `(tail A)` crashes.

    | ((tail (quote tail)) (tail (quote tail)) ifeq)
    ? 

`(cons A B)` evaluates A to a S-expression and B to a list, and evaluates to a list
which is the same as B except it has an extra element on the front, B.

    | ((cons (quote quote) (quote (head tail ifeq))) (cons (quote quote) (quote (head tail ifeq))) ifeq)
    = (quote head tail ifeq)

`(ifeq A B C D)` evaluates A and B; if they evaluate to the same atom
then this form evaluates to what C evaluates to, otherwise it evaluates to
what D evaluates to.

    | ((ifeq (quote head) (quote head) (quote cons) (quote self))
    |  (ifeq (quote head) (quote head) (quote cons) (quote self)) tail)
    = cons

    | ((ifeq (quote head) (quote tail) (quote cons) (quote self))
    |  (ifeq (quote head) (quote tail) (quote cons) (quote self)) tail)
    = self

`arg` evaluates to the argument of the current program-function.

    | (arg arg ifeq)
    = ifeq

    | ((tail arg) (tail arg) (ifeq ifeq (ifeq ifeq)))
    = (ifeq (ifeq ifeq))

`(self A)` evaluates A to an S-expression, then evaluates the main
program-function with that as the argument, and evaluates to the result
of that.

    | ((ifeq (head arg) (quote ifeq) arg (self (tail arg)))
    |  (ifeq (head arg) (quote ifeq) arg (self (tail arg)))
    |  (head head ifeq tail tail))
    = (ifeq tail tail)

Discussion
----------

### Comparison to Pixley ###

Yolk is quite similar to Pixley.  The main differences between Pixley and
Yolk are:

*   Yolk is not a subset of R5RS Scheme
*   Yolk was designed in a completely different fashion

In the first version of Yolk, `if` and `eq` were different forms.  I wrote
a meta-circular interpreter with that version, and measured it using `stats.scm`
from the Pixley distribution:

    Cons cells: 296
    Symbol instances: 169
    Unique symbols: 8 (cons self tail quote arg head eq if)

Then I realized that the first argument of `if` was always an `eq`, so merged
them into `ifeq`, and that the MCI could be simplified a tiny bit for the error
case, and that version is what is presented here.  It measures out to be:

    Cons cells: 255
    Symbol instances: 146
    Unique symbols: 7 (cons self tail quote arg head ifeq)

I then noticed that the second argument to `if` was always a `quote`, but
realized, when trying to change it so that it did not evaluate its second
argument, that it would no longer be possible to write an MCI in the resulting
language (explaining why this is, is left as an exercise for the reader.)

For comparison, the latest version of `pixley.pix`, as of this writing, has

    Cons cells: 684
    Symbol instances: 413
    Unique symbols: 54

Since Yolk is very similar to Pixley, but has a much smaller meta-circular
definition, an argument could definitely be made that its name should be
Hooterville — but that's not such a great name for a programming language.

On the other hand, the Yolk MCI has a less interesting (IMO) depiction as
nested rectangles a la Pixley.  That is not to say there isn't some possible
graphical depiction that makes the Yolk MCI look pretty, of course.

### Computational class ###

Yolk is almost certainly Turing-complete.  That, in itself, is not terribly
interesting; what is more interesting is how we can come to that conclusion
without the usual devices (giving a map from Yolk programs to Turing machines,
or implementing a universal Turing machine in Yolk.)

Yolk came about from my interest in whether there are any universal
computational classes which are not Turing-complete.  "Universal" in this
sense means something like, if M is in class C and M can simulate any other
member of class C then M is universal.

We know that there is a universal Turing machine.  We also know that there
is no universal primitive recursive function.  (There is a total function
which can simulate any PR function, but that function isn't itself PR.)

And we haven't yet found a computational class that is contained in PR that
is universal; they all admit to various diagonalizations and pumping lemmas
and such, and the function that can simulate any member of C is always, it
seems, somewhere outside C.

But are there any classes between PR and RE (the class of Turing machines)
that are universal?  It seems likely.

In fact, R (the class of Turing machines which always halt) qualifies in some
sense: if I always give a UTM only descriptions of TMs that always halt, then
that UTM always halts.  (Of course, that doesn't address the question of how
that UTM would prevent itself from trying to simulate a TM that doesn't halt
if it were given one.)

In a similar vein, it seems possible that linear-bounded automata might be
universal: if it takes a UTM at most (say) 18 steps to simulate one TM
transition, then, given a description of a linear-bounded TM on input, the
UTM's run time should bounded linearly too.  (Well, maybe.  The input on which
the bounds are based is now (data+machine_description) instead of just
(data)... anyway I haven't thought about it very much and it is more or less
a distraction from my main point.)

The thing is that PR and RE both have simple, "syntactic" definitions.
You can tell a PR computation or a RE computation just from its surface
structure.  But every class between them has a more complex, "semantic"
definition.  You need some extra machinery to tell if the machine being
simulated really belongs to the class or not — you need to prove it always
halts, or prove that it finishes within a linear bound of its input, or
whatnot.

Yolk's meta-circular interpreter can interpret itself, and, because it is
written in a general way, it can interpret any other Yolk program, too, making
it a universal Yolk interpreter.  Yet it has none of this extra machinery
that would be required for it to be above PR yet below RE.  So the functions
it can interpret must be all of those in RE; i.e. Yolk is Turing-complete.

THAT IS, OF COURSE, NOT A PROOF.

But on the other hand you can look at the Yolk instructions and probably
satisfy yourself that it would not be difficult to write a Tag machine in
Yolk.  It can locate data (`arg`, `head`, `tail`, `quote`), it can make
decisions based on that data (`ifeq`), and it can repeat this process with
different data (`self`).

In fact, the interesting thing is `cons`.

### `cons` ###

We can, in fact, re-write the initial sketch of the self-interpreter without
handling `cons` at all, because `cons` is only used in the definition of
`cons`:

    (ifeq arg (quote arg)
        arg
        (ifeq (head arg) (quote head)
            (head (self (head (tail arg))))
            (ifeq (head arg) (quote tail)
                (tail (self (head (tail arg))))
                (ifeq (head arg) (quote quote)
                    (head (tail arg))
                    (ifeq (head arg) (quote ifeq)
                        (ifeq (self (head (tail arg)))
                            (self (head (tail (tail arg))))
                            (self (head (tail (tail (tail arg)))))
                            (self (head (tail (tail (tail (tail arg)))))))
                        (ifeq (head arg) (quote self)
                            (self (self (head (tail arg))))
                            (ifeq))))))))

And you'd think, maybe, this can interpret itself.  And, maybe, that because
it works on smaller and smaller data each time, it is primitive recursive
(a la Exanoke.)  Except, no.  The definition of `self` in the sketch is wrong,
really quite wrong.  And to fix it, you need to be able to hold multiple
data in `arg`, and take it apart to find the code vs. the real data, and put
it back together again — and to put it back together again, you need `cons`.

Or something like `cons`, obviously; I played with various variations but
realized they all allow you to "grow" an S-expression.

Now, maybe I just didn't play with them *enough*.  Maybe we can define some
sort of `cons` that imposes some sort of restriction on its result not being
"bigger" than its input, except when used a certain way, somehow, in `self`
especially, so that... it all works out and it's universal but it's not
Turing-complete.

But I would be willing to bet that the meta-circular interpreter for that,
even if it exists, would be quite a bit larger than this.

(Happy Happy)!  
Chris Pressey  
London, UK  
August 24th, 2014
