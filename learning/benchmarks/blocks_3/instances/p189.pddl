;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=189, seed=9

(define (problem blocksworld-189)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b5)
    (on-table b5)
    (clear b3)
    (on-table b3)
    (clear b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b4)
    (on b4 b1)
    (on b1 b5)
    (on-table b5)
    (clear b2)
    (on-table b2))))
