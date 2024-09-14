;; cars=1, locations=3, seed=15, instance_id=45, out_folder=.

(define (problem ferry-45)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc3)
    (at car1 loc3)
)
 (:goal  (and (at car1 loc1))))
