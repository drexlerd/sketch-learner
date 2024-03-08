;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=181, seed=1

(define (problem blocksworld-181)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b1)
    (on b1 b2)
    (on b2 b5)
    (on b5 b4)
    (on b4 b3)
    (on-table b3))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b3)
    (on-table b3)
    (clear b1)
    (on b1 b5)
    (on b5 b4)
    (on-table b4))))
