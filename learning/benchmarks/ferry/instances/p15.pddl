;; cars=1, locations=2, seed=15, instance_id=15, out_folder=.

(define (problem ferry-15)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc2)
)
 (:goal  (and (at car1 loc1))))
