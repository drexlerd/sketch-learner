;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=356, seed=26

(define (problem blocksworld-356)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1)
    (clear b2)
    (on b2 b3)
    (on-table b3))))
