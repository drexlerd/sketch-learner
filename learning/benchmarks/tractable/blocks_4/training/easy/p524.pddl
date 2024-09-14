;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=524, seed=14

(define (problem blocksworld-524)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b4)
    (on b4 b5)
    (on b5 b2)
    (on-table b2)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b4)
    (on b4 b3)
    (on b3 b5)
    (on b5 b2)
    (on-table b2))))
