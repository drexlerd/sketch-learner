;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=183, seed=3

(define (problem blocksworld-183)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b4)
    (on-table b4)
    (clear b3)
    (on b3 b5)
    (on-table b5)
    (clear b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b4)
    (on b4 b5)
    (on-table b5)
    (clear b3)
    (on b3 b1)
    (on-table b1))))
