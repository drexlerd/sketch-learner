

(define (problem BW-rand-2)
(:domain blocksworld)
(:objects b2 )
(:init
(arm-empty)
(on b1 b2)
(on-table b2)
(clear b1)
)
(:goal
(and
(clear b1))
)
)


