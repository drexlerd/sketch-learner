;; blocks=2, percentage_new_tower=10, out_folder=., instance_id=54, seed=4

(define (problem blocksworld-54)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1)
    (clear b2)
    (on-table b2))))
