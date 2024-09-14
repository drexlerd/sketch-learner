;; cars=1, locations=2, seed=29, instance_id=29, out_folder=.

(define (problem ferry-29)
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
