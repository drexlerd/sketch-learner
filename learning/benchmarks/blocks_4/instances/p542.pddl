;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=542, seed=2

(define (problem blocksworld-542)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b4)
    (on b4 b2)
    (on b2 b5)
    (on b5 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on b3 b5)
    (on b5 b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))))
