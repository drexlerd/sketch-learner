;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=186, seed=6

(define (problem blocksworld-186)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on b3 b5)
    (on-table b5)
    (clear b4)
    (on-table b4)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b4)
    (on-table b4)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on b3 b2)
    (on b2 b5)
    (on-table b5))))
