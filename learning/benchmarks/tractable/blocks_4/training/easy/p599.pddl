;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=599, seed=29

(define (problem blocksworld-599)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on-table b3)
    (clear b5)
    (on-table b5)
    (clear b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b5)
    (on-table b5)
    (clear b3)
    (on b3 b4)
    (on b4 b1)
    (on-table b1))))
