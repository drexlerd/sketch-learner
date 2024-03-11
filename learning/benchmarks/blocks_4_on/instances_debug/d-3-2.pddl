

(define (problem BW-rand-3)
(:domain blocksworld)
(:objects b3 )
(:init
(arm-empty)
(on-table b2)
(on b3 b2)
(on b1 b3)
(clear b1)
)
(:goal
(and
(on b1 b2))
)
)


