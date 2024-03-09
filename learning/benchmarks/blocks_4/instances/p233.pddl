;; blocks=2, percentage_new_tower=40, out_folder=., instance_id=233, seed=23

(define (problem blocksworld-233)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on-table b2)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on-table b2))))
