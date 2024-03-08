;; blocks=2, percentage_new_tower=40, out_folder=., instance_id=78, seed=8

(define (problem blocksworld-78)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b1)
    (on-table b1))))
