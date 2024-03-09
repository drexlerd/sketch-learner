;; cars=3, locations=2, seed=3, instance_id=123, out_folder=.

(define (problem ferry-123)
 (:domain ferry)
 (:objects 
    car1 car2 car3 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc1)
    (at car2 loc2)
    (at car3 loc2)
)
 (:goal  (and (at car1 loc2)
   (at car2 loc1)
   (at car3 loc1))))
