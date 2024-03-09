;; cars=1, locations=2, seed=12, instance_id=12, out_folder=.

(define (problem ferry-12)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc1)
)
 (:goal  (and (at car1 loc2))))
