;; cars=2, locations=2, seed=22, instance_id=82, out_folder=.

(define (problem ferry-82)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc1)
    (at car2 loc1)
)
 (:goal  (and (at car1 loc2)
   (at car2 loc2))))
