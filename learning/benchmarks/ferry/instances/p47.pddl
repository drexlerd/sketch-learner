;; cars=1, locations=3, seed=17, instance_id=47, out_folder=.

(define (problem ferry-47)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc3)
)
 (:goal  (and (at car1 loc2))))
