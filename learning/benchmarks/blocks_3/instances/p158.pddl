;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=158, seed=8

(define (problem blocksworld-158)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b3)
    (on-table b3)
    (clear b2)
    (on-table b2)
    (clear b4)
    (on b4 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on b2 b4)
    (on-table b4))))
