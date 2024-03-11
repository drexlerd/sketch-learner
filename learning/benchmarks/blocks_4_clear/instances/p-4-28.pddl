

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b3 b4 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b1)
(on b3 b4)
(on-table b4)
(clear b2)
)
(:goal
(and
(clear b1))
)
)


