(define (problem grid-x3-y1-t2-k11-l11-p100)
(:domain grid)
(:objects 
        f0-0f f1-0f f2-0f 
        shape0 shape1 
        key0-0 
        key1-0 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(place f2-0f)
(shape shape0)
(shape shape1)
(key key0-0)
(key-shape key0-0 shape0)
(key key1-0)
(key-shape key1-0 shape1)
(conn f0-0f f1-0f)
(conn f1-0f f2-0f)
(conn f1-0f f0-0f)
(conn f2-0f f1-0f)
(open f0-0f)
(locked f2-0f)
(lock-shape f2-0f shape0)
(locked f1-0f)
(lock-shape f1-0f shape1)
(at key0-0 f2-0f)
(at key1-0 f2-0f)
(at-robot f0-0f)
)
(:goal
(and
(at key0-0 f2-0f)
(at key1-0 f2-0f)
)
)
)
