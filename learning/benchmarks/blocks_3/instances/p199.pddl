;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=199, seed=9

(define (problem blocksworld-199)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b1)
    (on-table b1)
    (clear b3)
    (on-table b3)
    (clear b4)
    (on-table b4)
    (clear b5)
    (on b5 b2)
    (on-table b2))
 (:goal  (and 
    (clear b5)
    (on b5 b2)
    (on b2 b3)
    (on-table b3)
    (clear b1)
    (on b1 b4)
    (on-table b4))))
