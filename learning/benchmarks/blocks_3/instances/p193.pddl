;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=193, seed=3

(define (problem blocksworld-193)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b4)
    (on-table b4)
    (clear b3)
    (on b3 b5)
    (on b5 b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b4)
    (on-table b4)
    (clear b1)
    (on-table b1)
    (clear b5)
    (on b5 b3)
    (on-table b3))))
