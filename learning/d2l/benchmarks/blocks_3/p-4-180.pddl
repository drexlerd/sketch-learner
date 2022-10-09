

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b1 b2 b3 b4  - block)
(:init
(on b1 b2)
(on b2 b3)
(on-table b3)
(on-table b4)
(clear b1)
(clear b4)
)
(:goal
(and
(on b2 b4)
(on b4 b3))
)
)


