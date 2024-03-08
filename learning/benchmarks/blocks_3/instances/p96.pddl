;; blocks=3, percentage_new_tower=10, out_folder=., instance_id=96, seed=6

(define (problem blocksworld-96)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))))
