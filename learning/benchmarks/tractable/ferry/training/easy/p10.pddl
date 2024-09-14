;; cars=1, locations=2, seed=10, instance_id=10, out_folder=.

(define (problem ferry-10)
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
