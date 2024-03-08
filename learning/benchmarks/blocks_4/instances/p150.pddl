;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=150, seed=0

(define (problem blocksworld-150)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on-table b2)
    (clear b3)
    (on b3 b4)
    (on-table b4)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on-table b1)
    (clear b2)
    (on-table b2)
    (clear b3)
    (on-table b3))))
