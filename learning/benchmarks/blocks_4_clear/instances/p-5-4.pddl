

(define (problem BW-rand-5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5  - block)
(:init
(on b1 b3)
(on-table b2)
(on b3 b4)
(on b4 b5)
(on b5 b2)
(clear b1)
)
(:goal
(and
(clear b1))
)
)


