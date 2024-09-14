(define (problem grid-x3-y1-t1-k0-l0-p100)
(:domain grid)
(:objects 
        f0-0f f1-0f f2-0f 
        shape0 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(place f2-0f)
(shape shape0)
(conn f0-0f f1-0f)
(conn f1-0f f2-0f)
(conn f1-0f f0-0f)
(conn f2-0f f1-0f)
(open f0-0f)
(open f1-0f)
(open f2-0f)
(at-robot f2-0f)
)
(:goal
(and
)
)
)
