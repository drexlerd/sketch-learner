

(define (problem BW-rand-5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5  - block)
(:init
(on b1 b4)
(on-table b2)
(on-table b3)
(on b4 b5)
(on b5 b2)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b4)
(on b4 b5)
(clear b1)
(clear b2)
(clear b3))
)
)


