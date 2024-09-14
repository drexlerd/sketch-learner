;; blocks=4, percentage_new_tower=10, out_folder=., instance_id=393, seed=3

(define (problem blocksworld-393)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b1)
    (on b1 b3)
    (on-table b3)
    (clear b4)
    (on-table b4))
 (:goal  (and 
    (clear b4)
    (on-table b4)
    (clear b2)
    (on b2 b1)
    (on b1 b3)
    (on-table b3))))
