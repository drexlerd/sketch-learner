;; cars=1, locations=2, seed=9, instance_id=9, out_folder=.

(define (problem ferry-09)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc2)
)
 (:goal  (and (at car1 loc1))))
