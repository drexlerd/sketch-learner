;; blocks=1, percentage_new_tower=10, out_folder=., instance_id=18, seed=8

(define (problem blocksworld-18)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
