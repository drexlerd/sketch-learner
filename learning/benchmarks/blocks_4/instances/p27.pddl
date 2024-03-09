;; blocks=1, percentage_new_tower=0, out_folder=., instance_id=27, seed=27

(define (problem blocksworld-27)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
