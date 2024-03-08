;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=185, seed=5

(define (problem blocksworld-185)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b1)
    (on-table b1)
    (clear b5)
    (on-table b5)
    (clear b2)
    (on b2 b4)
    (on-table b4))
 (:goal  (and 
    (clear b2)
    (on b2 b5)
    (on b5 b3)
    (on b3 b4)
    (on b4 b1)
    (on-table b1))))
