

(define (problem BW-rand-4)
(:domain blocksworld)
(:objects b2 b3 b4 )
(:init
(arm-empty)
(on b1 b3)
(on-table b2)
(on b3 b4)
(on b4 b2)
(clear b1)
)
(:goal
(and
(clear b1))
)
)


