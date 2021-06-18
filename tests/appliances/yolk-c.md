This Falderal appliance tests the compiled-with-RPython version of the Yolk
reference interpreter.

This requires `fa-under-pty`, which is a part of Falderal since version 0.10.

It requires `fa-under-pty` because, for whatever reason, executables produced
by RPython from PyPy version 7.3.5 do not handle having their stdout redirected
very well.  Specifically, they dump core.  It is for this very reason that
`fa-under-pty` was written, in fact.

    -> Functionality "Evaluate Yolk program" is implemented by
    -> shell command
    -> "./script/fa-under-pty ./bin/yolk-c %(test-body-file) -i %(test-input-file)"

    -> Functionality "Evaluate Yolk program with MCI Sketch" is implemented by
    -> shell command
    -> "./script/fa-under-pty ./bin/yolk-c eg/mci-sketch.yolk -i %(test-body-file)"

    -> Functionality "Evaluate Yolk program with MCI with arg" is implemented by
    -> shell command
    -> "./script/fa-under-pty ./bin/yolk-c eg/mci-with-arg.yolk -i %(test-body-file)"

    -> Functionality "Evaluate Yolk program with MCI" is implemented by
    -> shell command
    -> "./script/fa-under-pty ./bin/yolk-c eg/yolk.yolk -i %(test-body-file)"
