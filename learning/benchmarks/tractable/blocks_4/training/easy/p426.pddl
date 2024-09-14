;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=426, seed=6

(define (problem blocksworld-426)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b3)
    (on b3 b2)
    (on b2 b4)
    (on-table b4))
 (:goal  (and 
    (clear b3)
    (on b3 b4)
    (on b4 b1)
    (on b1 b2)
    (on-table b2))))
