;; blocks=1, percentage_new_tower=10, out_folder=., instance_id=59, seed=29

(define (problem blocksworld-59)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
