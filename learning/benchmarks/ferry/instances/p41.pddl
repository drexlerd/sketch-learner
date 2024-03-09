;; cars=1, locations=3, seed=11, instance_id=41, out_folder=.

(define (problem ferry-41)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc3)
    (at car1 loc2)
)
 (:goal  (and (at car1 loc3))))
