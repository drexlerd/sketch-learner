;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=513, seed=3

(define (problem blocksworld-513)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b5)
    (on b5 b4)
    (on b4 b3)
    (on b3 b2)
    (on-table b2))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on-table b1)
    (clear b5)
    (on b5 b3)
    (on b3 b2)
    (on-table b2))))
