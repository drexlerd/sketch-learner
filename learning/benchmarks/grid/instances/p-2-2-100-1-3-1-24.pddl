(define (problem grid-x3-y1-t1-k2-l2-p100)
(:domain grid)
(:objects 
        f0-0f f1-0f f2-0f 
        shape0 
        key0-0 key0-1 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(place f2-0f)
(shape shape0)
(key key0-0)
(key-shape key0-0 shape0)
(key key0-1)
(key-shape key0-1 shape0)
(conn f0-0f f1-0f)
(conn f1-0f f2-0f)
(conn f1-0f f0-0f)
(conn f2-0f f1-0f)
(open f1-0f)
(locked f0-0f)
(lock-shape f0-0f shape0)
(locked f2-0f)
(lock-shape f2-0f shape0)
(at key0-0 f1-0f)
(at key0-1 f2-0f)
(at-robot f1-0f)
)
(:goal
(and
(at key0-0 f2-0f)
(at key0-1 f2-0f)
)
)
)
