;; blocks=5, percentage_new_tower=0, out_folder=., instance_id=168, seed=8

(define (problem blocksworld-168)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b5)
    (on b5 b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b5)
    (on b5 b1)
    (on b1 b3)
    (on b3 b4)
    (on b4 b2)
    (on-table b2))))
