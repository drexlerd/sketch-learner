;; blocks=3, percentage_new_tower=10, out_folder=., instance_id=286, seed=16

(define (problem blocksworld-286)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b1)
    (on b1 b2)
    (on-table b2))))
