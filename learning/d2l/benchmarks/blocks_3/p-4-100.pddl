

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b1 b2 b3 b4  - block)
(:init
(on b1 b3)
(on-table b2)
(on b3 b4)
(on b4 b2)
(clear b1)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b4 b3))
)
)


