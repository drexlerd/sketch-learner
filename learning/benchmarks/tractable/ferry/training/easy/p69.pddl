;; cars=2, locations=2, seed=9, instance_id=69, out_folder=.

(define (problem ferry-69)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc2)
    (at car2 loc2)
)
 (:goal  (and (at car1 loc1)
   (at car2 loc1))))
