

(define (problem BW-rand-5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 )
(:init
(arm-empty)
(on b1 b5)
(on-table b2)
(on b3 b4)
(on b4 b2)
(on b5 b3)
(clear b1)
)
(:goal
(and
(clear b1))
)
)


