;; cars=1, locations=2, seed=5, instance_id=5, out_folder=.

(define (problem ferry-05)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc1)
)
 (:goal  (and (at car1 loc2))))
