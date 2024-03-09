;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=461, seed=11

(define (problem blocksworld-461)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1)
    (clear b4)
    (on-table b4)
    (clear b3)
    (on-table b3)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b4)
    (on-table b4)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on-table b3))))
