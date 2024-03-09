;; cars=2, locations=3, seed=16, instance_id=106, out_folder=.

(define (problem ferry-106)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc1)
    (at car2 loc3)
)
 (:goal  (and (at car1 loc3)
   (at car2 loc2))))
