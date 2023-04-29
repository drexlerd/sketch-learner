

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b1 b2 b3 b4  - block)
(:init
(on b1 b4)
(on-table b2)
(on-table b3)
(on b4 b2)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b4))
)
)


