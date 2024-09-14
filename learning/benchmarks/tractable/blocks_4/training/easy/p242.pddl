;; blocks=3, percentage_new_tower=0, out_folder=., instance_id=242, seed=2

(define (problem blocksworld-242)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on b3 b2)
    (on b2 b1)
    (on-table b1))))
