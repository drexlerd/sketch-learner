;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=119, seed=9

(define (problem blocksworld-119)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b1)
    (on b1 b2)
    (on-table b2)
    (clear b3)
    (on-table b3))
 (:goal  (and 
    (clear b3)
    (on b3 b1)
    (on b1 b2)
    (on-table b2))))
