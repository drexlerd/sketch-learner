;; blocks=1, percentage_new_tower=20, out_folder=., instance_id=24, seed=4

(define (problem blocksworld-24)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
