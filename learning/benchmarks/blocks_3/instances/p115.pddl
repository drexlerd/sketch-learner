;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=115, seed=5

(define (problem blocksworld-115)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on b2 b3)
    (on-table b3))
 (:goal  (and 
    (clear b2)
    (on b2 b3)
    (on-table b3)
    (clear b1)
    (on-table b1))))
