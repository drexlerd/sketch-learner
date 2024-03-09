;; cars=1, locations=2, seed=19, instance_id=19, out_folder=.

(define (problem ferry-19)
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
