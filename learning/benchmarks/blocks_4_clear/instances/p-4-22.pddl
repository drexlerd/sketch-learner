

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b2 b3 b4 )
(:init
(arm-empty)
(on b1 b3)
(on-table b2)
(on b3 b2)
(on-table b4)
(clear b1)
(clear b4)
)
(:goal
(and
(clear b1))
)
)


