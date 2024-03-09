;; blocks=1, percentage_new_tower=0, out_folder=., instance_id=28, seed=28

(define (problem blocksworld-28)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
