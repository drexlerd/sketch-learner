;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=198, seed=8

(define (problem blocksworld-198)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b2)
    (on-table b2)
    (clear b3)
    (on b3 b5)
    (on-table b5)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on b3 b1)
    (on-table b1)
    (clear b4)
    (on b4 b5)
    (on b5 b2)
    (on-table b2))))
