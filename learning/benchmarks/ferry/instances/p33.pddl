;; cars=2, locations=3, seed=3, instance_id=33, out_folder=.

(define (problem ferry-33)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc1)
    (at car2 loc2)
)
 (:goal  (and (at car1 loc2)
   (at car2 loc3))))
