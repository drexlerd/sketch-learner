;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=194, seed=4

(define (problem blocksworld-194)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on-table b3)
    (clear b4)
    (on b4 b2)
    (on-table b2)
    (clear b5)
    (on b5 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b5)
    (on b5 b1)
    (on b1 b4)
    (on-table b4)
    (clear b2)
    (on-table b2))))
