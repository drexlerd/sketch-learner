;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=456, seed=6

(define (problem blocksworld-456)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b3)
    (on b3 b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b1)
    (on b1 b4)
    (on b4 b2)
    (on-table b2))))
