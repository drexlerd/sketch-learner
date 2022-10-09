

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b1 b2 b3 b4  - block)
(:init
(on-table b1)
(on-table b2)
(on-table b3)
(on b4 b3)
(clear b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b3 b2)
(on b4 b3))
)
)


