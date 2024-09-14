;; cars=2, locations=3, seed=22, instance_id=112, out_folder=.

(define (problem ferry-112)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc2)
    (at car2 loc3)
)
 (:goal  (and (at car1 loc1)
   (at car2 loc1))))
