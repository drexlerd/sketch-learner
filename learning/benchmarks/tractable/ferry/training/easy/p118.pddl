;; cars=2, locations=3, seed=28, instance_id=118, out_folder=.

(define (problem ferry-118)
 (:domain ferry)
 (:objects 
    car1 car2 - car
    loc1 loc2 loc3 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc1)
    (at car2 loc2)
)
 (:goal  (and (at car1 loc3)
   (at car2 loc3))))
