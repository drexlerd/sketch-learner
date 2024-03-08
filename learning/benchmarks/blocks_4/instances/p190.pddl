;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=190, seed=0

(define (problem blocksworld-190)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on b1 b4)
    (on-table b4)
    (clear b5)
    (on-table b5))
 (:goal  (and 
    (clear b5)
    (on-table b5)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on b2 b3)
    (on b3 b4)
    (on-table b4))))
