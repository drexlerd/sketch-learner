;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=455, seed=5

(define (problem blocksworld-455)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b2)
    (on b2 b4)
    (on-table b4)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on b3 b2)
    (on-table b2)
    (clear b1)
    (on b1 b4)
    (on-table b4))))
