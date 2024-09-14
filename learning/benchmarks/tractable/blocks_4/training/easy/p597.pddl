;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=597, seed=27

(define (problem blocksworld-597)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on-table b3)
    (clear b5)
    (on b5 b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b5)
    (on b5 b3)
    (on b3 b2)
    (on b2 b4)
    (on-table b4)
    (clear b1)
    (on-table b1))))
