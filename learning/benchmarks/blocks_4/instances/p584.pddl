;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=584, seed=14

(define (problem blocksworld-584)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on b3 b5)
    (on-table b5)
    (clear b1)
    (on b1 b4)
    (on-table b4))
 (:goal  (and 
    (clear b5)
    (on b5 b2)
    (on-table b2)
    (clear b3)
    (on-table b3)
    (clear b1)
    (on b1 b4)
    (on-table b4))))
