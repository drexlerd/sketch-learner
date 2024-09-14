(define (problem grid-x1-y3-t2-k2-l2-p50)
(:domain grid)
(:objects 
        f0-0f 
        f0-1f 
        f0-2f 
        shape0 shape1 
        key1-0 key1-1 
)
(:init
(arm-empty)
(place f0-0f)
(place f0-1f)
(place f0-2f)
(shape shape0)
(shape shape1)
(key key1-0)
(key-shape key1-0 shape1)
(key key1-1)
(key-shape key1-1 shape1)
(conn f0-0f f0-1f)
(conn f0-1f f0-2f)
(conn f0-1f f0-0f)
(conn f0-2f f0-1f)
(open f0-0f)
(locked f0-2f)
(lock-shape f0-2f shape1)
(locked f0-1f)
(lock-shape f0-1f shape1)
(at key1-0 f0-0f)
(at key1-1 f0-0f)
(at-robot f0-0f)
)
(:goal
(and
)
)
)
