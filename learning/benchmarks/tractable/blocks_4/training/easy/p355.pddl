;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=355, seed=25

(define (problem blocksworld-355)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on-table b2)
    (clear b3)
    (on-table b3)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1)
    (clear b3)
    (on-table b3)
    (clear b2)
    (on-table b2))))
