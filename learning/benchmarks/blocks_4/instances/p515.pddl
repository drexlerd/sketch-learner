;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=515, seed=5

(define (problem blocksworld-515)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on-table b3)
    (clear b4)
    (on b4 b5)
    (on b5 b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b4)
    (on-table b4)
    (clear b3)
    (on b3 b1)
    (on b1 b2)
    (on-table b2)
    (clear b5)
    (on-table b5))))
