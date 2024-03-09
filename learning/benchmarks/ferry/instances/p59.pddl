;; cars=1, locations=3, seed=29, instance_id=59, out_folder=.

(define (problem ferry-59)
 (:domain ferry)
 (:objects 
    car1 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc3)
    (at car1 loc1)
)
 (:goal  (and (at car1 loc3))))
