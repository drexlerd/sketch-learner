

(define (problem BW-rand-3)
(:domain blocksworld)
(:objects b2 b3 )
(:init
(arm-empty)
(on-table b1)
(on b2 b3)
(on b3 b1)
(clear b2)
)
(:goal
(and
(clear b1))
)
)


