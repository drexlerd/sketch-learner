;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=598, seed=28

(define (problem blocksworld-598)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b5)
    (on b5 b1)
    (on-table b1)
    (clear b2)
    (on b2 b4)
    (on-table b4))
 (:goal  (and 
    (clear b3)
    (on b3 b2)
    (on b2 b5)
    (on b5 b1)
    (on-table b1)
    (clear b4)
    (on-table b4))))
