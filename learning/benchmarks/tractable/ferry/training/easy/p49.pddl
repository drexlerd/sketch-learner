;; cars=1, locations=3, seed=19, instance_id=49, out_folder=.

(define (problem ferry-49)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc3)
)
 (:goal  (and (at car1 loc2))))
