;; vehicles=4, packages=6, locations=9, max_capacity=2, out_folder=training/easy, instance_id=34, seed=75

(define (problem transport-34)
 (:domain transport)
 (:objects 
    v1 v2 v3 v4 - vehicle
    p1 p2 p3 p4 p5 p6 - package
    l1 l2 l3 l4 l5 l6 l7 l8 l9 - location
    c0 c1 c2 - size
    )
 (:init (capacity v1 c2)
    (capacity v2 c2)
    (capacity v3 c2)
    (capacity v4 c1)
    (capacity-predecessor c0 c1)
    (capacity-predecessor c1 c2)
    (at p1 l9)
    (at p2 l8)
    (at p3 l6)
    (at p4 l2)
    (at p5 l6)
    (at p6 l2)
    (at v1 l5)
    (at v2 l5)
    (at v3 l8)
    (at v4 l6)
    (road l7 l4)
    (road l6 l2)
    (road l6 l5)
    (road l5 l8)
    (road l3 l7)
    (road l9 l2)
    (road l7 l3)
    (road l2 l3)
    (road l2 l9)
    (road l4 l7)
    (road l8 l5)
    (road l2 l6)
    (road l5 l6)
    (road l3 l2)
    (road l9 l1)
    (road l1 l9)
    )
 (:goal  (and 
    (at p1 l1)
    (at p2 l5)
    (at p3 l8)
    (at p4 l5)
    (at p5 l1)
    (at p6 l9))))
