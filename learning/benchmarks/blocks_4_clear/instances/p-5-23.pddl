

(define (problem BW-rand-5)
(:domain blocksworld)
(:objects b3 b4 b5 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b1)
(on b3 b5)
(on-table b4)
(on-table b5)
(clear b2)
(clear b4)
)
(:goal
(and
(clear b1))
)
)


