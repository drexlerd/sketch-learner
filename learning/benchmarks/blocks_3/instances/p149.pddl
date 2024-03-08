;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=149, seed=9

(define (problem blocksworld-149)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b1)
    (on b1 b2)
    (on-table b2)
    (clear b3)
    (on-table b3))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on b1 b3)
    (on b3 b2)
    (on-table b2))))
