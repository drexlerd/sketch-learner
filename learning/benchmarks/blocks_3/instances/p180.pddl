;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=180, seed=0

(define (problem blocksworld-180)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b5)
    (on b5 b3)
    (on b3 b1)
    (on-table b1)
    (clear b2)
    (on-table b2)
    (clear b4)
    (on-table b4))
 (:goal  (and 
    (clear b3)
    (on b3 b1)
    (on b1 b5)
    (on b5 b2)
    (on-table b2)
    (clear b4)
    (on-table b4))))
