;; blocks=1, percentage_new_tower=40, out_folder=., instance_id=101, seed=11

(define (problem blocksworld-101)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
