; An implementation of Yolk in Scheme.
; This is mostly illustrative.

(define head car)
(define tail cdr)

(define eval-yolk (lambda (full prog arg)
  (cond
    ((eq? prog 'arg)
      arg)
    ((eq? (head prog) 'head)
      (head
        (eval-yolk full (head (tail prog)) arg)))
    ((eq? (head prog) 'tail)
      (tail
        (eval-yolk full (head (tail prog)) arg)))
    ((eq? (head prog) 'cons)
      (cons
        (eval-yolk full (head (tail prog)) arg)
        (eval-yolk full (head (tail (tail prog))) arg)))
    ((eq? (head prog) 'quote)
      (head (tail prog)))
    ((eq? (head prog) 'ifeq)
      (if
        (eq? (eval-yolk full (head (tail prog)) arg)
             (eval-yolk full (head (tail (tail prog))) arg))
        (eval-yolk full (head (tail (tail (tail prog)))) arg)
        (eval-yolk full (head (tail (tail (tail (tail prog))))) arg)))
    ((eq? (head prog) 'self)
      (eval-yolk full full (eval-yolk full (head (tail prog) arg))))
    (else
      (head 'head)))))
