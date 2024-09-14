(define (problem grid-x1-y2-t1-k1-l1-p100)
(:domain grid)
(:objects 
        f0-0f 
        f0-1f 
        shape0 
        key0-0 
)
(:init
(arm-empty)
(place f0-0f)
(place f0-1f)
(shape shape0)
(key key0-0)
(key-shape key0-0 shape0)
(conn f0-0f f0-1f)
(conn f0-1f f0-0f)
(open f0-0f)
(locked f0-1f)
(lock-shape f0-1f shape0)
(at key0-0 f0-0f)
(at-robot f0-0f)
)
(:goal
(and
(at key0-0 f0-1f)
)
)
)
