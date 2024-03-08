;; blocks=4, percentage_new_tower=10, out_folder=., instance_id=134, seed=4

(define (problem blocksworld-134)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b2)
    (on b2 b1)
    (on b1 b3)
    (on-table b3)
    (clear b4)
    (on-table b4))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b2)
    (on b2 b1)
    (on-table b1)
    (clear b4)
    (on-table b4))))
