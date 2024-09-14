;; blocks=2, percentage_new_tower=20, out_folder=., instance_id=186, seed=6

(define (problem blocksworld-186)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b1)
    (on-table b1))))
