;; blocks=3, percentage_new_tower=20, out_folder=., instance_id=109, seed=9

(define (problem blocksworld-109)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b3)
    (on b3 b2)
    (on-table b2)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))))
