(define (problem grid-x2-y2-t2-k2-l2-p0)
(:domain grid)
(:objects 
        f0-0f f1-0f 
        f0-1f f1-1f 
        shape0 shape1 
        key1-0 key1-1 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(place f0-1f)
(place f1-1f)
(shape shape0)
(shape shape1)
(key key1-0)
(key-shape key1-0 shape1)
(key key1-1)
(key-shape key1-1 shape1)
(conn f0-0f f1-0f)
(conn f0-1f f1-1f)
(conn f0-0f f0-1f)
(conn f1-0f f1-1f)
(conn f1-0f f0-0f)
(conn f1-1f f0-1f)
(conn f0-1f f0-0f)
(conn f1-1f f1-0f)
(open f0-0f)
(open f0-1f)
(locked f1-0f)
(lock-shape f1-0f shape1)
(locked f1-1f)
(lock-shape f1-1f shape1)
(at key1-0 f0-1f)
(at key1-1 f0-0f)
(at-robot f0-0f)
)
(:goal
(and
)
)
)
