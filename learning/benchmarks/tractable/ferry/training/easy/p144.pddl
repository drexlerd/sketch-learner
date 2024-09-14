;; cars=3, locations=2, seed=24, instance_id=144, out_folder=.

(define (problem ferry-144)
 (:domain ferry)
 (:objects 
    car1 car2 car3 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc2)
    (at car2 loc1)
    (at car3 loc2)
)
 (:goal  (and (at car1 loc1)
   (at car2 loc2)
   (at car3 loc1))))
