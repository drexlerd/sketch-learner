;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=359, seed=29

(define (problem blocksworld-359)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b1)
    (on b1 b3)
    (on-table b3))
 (:goal  (and 
    (clear b2)
    (on b2 b1)
    (on-table b1)
    (clear b3)
    (on-table b3))))
