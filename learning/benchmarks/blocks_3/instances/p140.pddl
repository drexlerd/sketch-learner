;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=140, seed=0

(define (problem blocksworld-140)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b1)
    (on b1 b3)
    (on-table b3)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b3)
    (on b3 b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))))
