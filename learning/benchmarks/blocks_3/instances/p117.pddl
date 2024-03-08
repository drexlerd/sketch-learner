;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=117, seed=7

(define (problem blocksworld-117)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b2)
    (on-table b2)
    (clear b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b3)
    (on b3 b1)
    (on-table b1))))
