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
      (eval-yolk full full (eval-yolk full (head (tail prog)) arg)))
    (else
      (head 'head)))))

; A rewriting of the above in continuation-passing style.

(define eval-yolk-k (lambda (full prog arg k)
  (cond
    ((eq? prog 'arg)
      (k arg))
    ((eq? (head prog) 'head)
      (eval-yolk-k full (head (tail prog)) arg (lambda (r) (k (head r)))))
    ((eq? (head prog) 'tail)
      (eval-yolk-k full (head (tail prog)) arg (lambda (r) (k (tail r)))))
    ((eq? (head prog) 'cons)
      (eval-yolk-k full (head (tail prog)) arg (lamdba (h)
        (eval-yolk-k full (head (tail (tail prog))) arg (lambda (t)
          (k (cons h t)))))))
    ((eq? (head prog) 'quote)
      (k (head (tail prog))))
    ((eq? (head prog) 'ifeq)
      (eval-yolk-k full (head (tail prog)) arg (lambda (a)
        (eval-yolk-k full (head (tail (tail prog))) arg (lambda (b)
          (if (eq? a b)
            (eval-yolk-k full (head (tail (tail (tail prog)))) arg k)
            (eval-yolk-k full (head (tail (tail (tail (tail prog))))) arg k)))))))
    ((eq? (head prog) 'self)
      (eval-yolk-k full (head (tail prog)) arg (lambda (newarg)
        (eval-yolk-k full full newarg k))))
    (else
      (k (head 'head))))))
