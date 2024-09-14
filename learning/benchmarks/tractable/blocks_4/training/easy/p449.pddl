;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=449, seed=29

(define (problem blocksworld-449)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on-table b4)
    (clear b2)
    (on b2 b1)
    (on b1 b3)
    (on-table b3))
 (:goal  (and 
    (clear b3)
    (on b3 b2)
    (on b2 b4)
    (on b4 b1)
    (on-table b1))))
