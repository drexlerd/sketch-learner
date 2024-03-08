;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=155, seed=5

(define (problem blocksworld-155)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b4)
    (on-table b4)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on b2 b3)
    (on-table b3))
 (:goal  (and 
    (clear b1)
    (on-table b1)
    (clear b4)
    (on b4 b2)
    (on b2 b3)
    (on-table b3))))
