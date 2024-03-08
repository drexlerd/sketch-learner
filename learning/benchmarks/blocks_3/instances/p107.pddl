;; blocks=3, percentage_new_tower=20, out_folder=., instance_id=107, seed=7

(define (problem blocksworld-107)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b1)
    (on-table b1)
    (clear b2)
    (on-table b2)
    (clear b3)
    (on-table b3))
 (:goal  (and 
    (clear b3)
    (on b3 b2)
    (on-table b2)
    (clear b1)
    (on-table b1))))
