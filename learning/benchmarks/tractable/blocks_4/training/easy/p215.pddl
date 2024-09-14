;; blocks=2, percentage_new_tower=40, out_folder=., instance_id=215, seed=5

(define (problem blocksworld-215)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b1)
    (on-table b1)
    (clear b2)
    (on-table b2))))
