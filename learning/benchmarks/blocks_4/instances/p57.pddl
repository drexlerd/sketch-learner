;; blocks=1, percentage_new_tower=10, out_folder=., instance_id=57, seed=27

(define (problem blocksworld-57)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
