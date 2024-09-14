;; cars=3, locations=3, seed=10, instance_id=160, out_folder=.

(define (problem ferry-160)
 (:domain ferry)
 (:objects 
    car1 car2 car3 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc1)
    (at car2 loc2)
    (at car3 loc2)
)
 (:goal  (and (at car1 loc2)
   (at car2 loc1)
   (at car3 loc1))))
