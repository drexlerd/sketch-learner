(define (problem BLOCKS-5-0)
(:domain blocksworld-atomic)
(:objects a b c d)

(:init
    (on a b)
    (on b c)
    (on c d)
    (on d table)
    (clear table)
    (clear a)

;; import itertools
;; _ = [print(f"(diff {b1} {b2})") for b1, b2 in itertools.permutations(['table'] + 'a b c'.split(), 2)]
    (diff table a)
    (diff table b)
    (diff table c)
    (diff table d)
    (diff a table)
    (diff a b)
    (diff a c)
    (diff a d)
    (diff b table)
    (diff b a)
    (diff b c)
    (diff b d)
    (diff c table)
    (diff c a)
    (diff c b)
    (diff c d)
    (diff d table)
    (diff d a)
    (diff d b)
    (diff d c)
)

; unstack tower on table and reverse partial tower on top of d
; in this instance, it is not allowed to unstack a on table then b on a then c on b because d at the bottom is missing
(:goal (and
	(on c b)
	(on b a)
    (on a d)
    (on d table)
))






)