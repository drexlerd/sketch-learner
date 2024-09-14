;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=440, seed=20

(define (problem blocksworld-440)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b1)
    (on-table b1)
    (clear b3)
    (on-table b3)
    (clear b4)
    (on-table b4))
 (:goal  (and 
    (clear b3)
    (on b3 b4)
    (on-table b4)
    (clear b2)
    (on b2 b1)
    (on-table b1))))
