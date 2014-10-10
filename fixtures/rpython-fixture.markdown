This Falderal fixture tests the compiled-with-RPython version of the Yolk
reference interpreter.

This requires `fa-under-pty`, which is a part of Falderal version 0.10.

It requires `fa-under-pty` because, for whatever reason, executables produced
by RPython from PyPy version 2.3.1 do not handle having their stdout redirected
very well.  Specifically, they dump core.  It is for this very reason that
`fa-under-pty` was written, in fact.

    -> Functionality "Evaluate Yolk program" is implemented by
    -> shell command
    -> "fa-under-pty ./yolk-c %(test-body-file) %(test-input-file)"
