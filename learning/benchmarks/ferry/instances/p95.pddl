;; cars=2, locations=3, seed=5, instance_id=95, out_folder=.

(define (problem ferry-95)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc2)
    (at car2 loc3)
)
 (:goal  (and (at car1 loc3)
   (at car2 loc2))))
