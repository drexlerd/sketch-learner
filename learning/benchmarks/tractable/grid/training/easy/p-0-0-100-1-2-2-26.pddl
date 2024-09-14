(define (problem grid-x2-y2-t1-k0-l0-p100)
(:domain grid)
(:objects 
        f0-0f f1-0f 
        f0-1f f1-1f 
        shape0 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(place f0-1f)
(place f1-1f)
(shape shape0)
(conn f0-0f f1-0f)
(conn f0-1f f1-1f)
(conn f0-0f f0-1f)
(conn f1-0f f1-1f)
(conn f1-0f f0-0f)
(conn f1-1f f0-1f)
(conn f0-1f f0-0f)
(conn f1-1f f1-0f)
(open f0-0f)
(open f1-0f)
(open f0-1f)
(open f1-1f)
(at-robot f1-0f)
)
(:goal
(and
)
)
)
