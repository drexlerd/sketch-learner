;; cars=3, locations=3, seed=0, instance_id=50, out_folder=.

(define (problem ferry-50)
 (:domain ferry)
 (:objects 
    car1 car2 car3 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc3)
    (at car2 loc1)
    (at car3 loc1)
)
 (:goal  (and (at car1 loc1)
   (at car2 loc3)
   (at car3 loc2))))
