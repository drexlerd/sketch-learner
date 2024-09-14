;; cars=1, locations=3, seed=26, instance_id=56, out_folder=.

(define (problem ferry-56)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc2)
)
 (:goal  (and (at car1 loc3))))
