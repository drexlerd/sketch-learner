;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=563, seed=23

(define (problem blocksworld-563)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on-table b4)
    (clear b2)
    (on b2 b3)
    (on-table b3)
    (clear b5)
    (on-table b5)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b5)
    (on b5 b3)
    (on b3 b2)
    (on b2 b1)
    (on-table b1)
    (clear b4)
    (on-table b4))))
