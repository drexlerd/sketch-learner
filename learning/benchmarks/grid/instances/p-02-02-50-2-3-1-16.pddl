(define (problem grid-x3-y1-t2-k2-l2-p50)
(:domain grid)
(:objects 
        f0-0f f1-0f f2-0f 
        shape0 shape1 
        key1-0 key1-1 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(place f2-0f)
(shape shape0)
(shape shape1)
(key key1-0)
(key-shape key1-0 shape1)
(key key1-1)
(key-shape key1-1 shape1)
(conn f0-0f f1-0f)
(conn f1-0f f2-0f)
(conn f1-0f f0-0f)
(conn f2-0f f1-0f)
(open f2-0f)
(locked f0-0f)
(lock-shape f0-0f shape1)
(locked f1-0f)
(lock-shape f1-0f shape1)
(at key1-0 f0-0f)
(at key1-1 f0-0f)
(at-robot f2-0f)
)
(:goal
(and
(at key1-0 f0-0f)
)
)
)
