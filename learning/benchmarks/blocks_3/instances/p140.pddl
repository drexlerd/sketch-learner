;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=140, seed=0

(define (problem blocksworld-140)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b1)
    (on b1 b4)
    (on b4 b3)
    (on b3 b2)
    (on-table b2))
 (:goal  (and 
    (clear b3)
    (on b3 b1)
    (on b1 b2)
    (on-table b2)
    (clear b4)
    (on-table b4))))
