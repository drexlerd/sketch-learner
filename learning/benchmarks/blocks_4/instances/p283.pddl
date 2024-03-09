;; blocks=3, percentage_new_tower=10, out_folder=., instance_id=283, seed=13

(define (problem blocksworld-283)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b3)
    (on-table b3)
    (clear b1)
    (on-table b1))))
