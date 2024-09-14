(define (problem grid-x2-y1-t1-k1-l1-p100)
(:domain grid)
(:objects 
        f0-0f f1-0f 
        shape0 
        key0-0 
)
(:init
(arm-empty)
(place f0-0f)
(place f1-0f)
(shape shape0)
(key key0-0)
(key-shape key0-0 shape0)
(conn f0-0f f1-0f)
(conn f1-0f f0-0f)
(open f0-0f)
(locked f1-0f)
(lock-shape f1-0f shape0)
(at key0-0 f1-0f)
(at-robot f0-0f)
)
(:goal
(and
(at key0-0 f0-0f)
)
)
)
