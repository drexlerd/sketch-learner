;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=116, seed=6

(define (problem blocksworld-116)
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
    (clear b2)
    (on-table b2)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on-table b3))))
