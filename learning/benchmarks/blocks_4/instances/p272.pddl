;; blocks=3, percentage_new_tower=10, out_folder=., instance_id=272, seed=2

(define (problem blocksworld-272)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b2)
    (on b2 b3)
    (on-table b3))
 (:goal  (and 
    (clear b1)
    (on b1 b3)
    (on-table b3)
    (clear b2)
    (on-table b2))))
