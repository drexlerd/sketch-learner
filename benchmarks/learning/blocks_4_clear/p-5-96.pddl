

(define (problem BW-rand-5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 )
(:init
(arm-empty)
(on b1 b5)
(on-table b2)
(on-table b3)
(on b4 b2)
(on-table b5)
(clear b1)
(clear b3)
(clear b4)
)
(:goal
(and
(clear b1))
)
)


