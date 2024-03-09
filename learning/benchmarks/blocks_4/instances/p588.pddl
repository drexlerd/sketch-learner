;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=588, seed=18

(define (problem blocksworld-588)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b5)
    (on b5 b4)
    (on b4 b1)
    (on b1 b3)
    (on-table b3))
 (:goal  (and 
    (clear b5)
    (on-table b5)
    (clear b3)
    (on-table b3)
    (clear b1)
    (on b1 b4)
    (on b4 b2)
    (on-table b2))))
