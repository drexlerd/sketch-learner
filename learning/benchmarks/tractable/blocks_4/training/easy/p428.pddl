;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=428, seed=8

(define (problem blocksworld-428)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b3)
    (on b3 b4)
    (on b4 b2)
    (on-table b2))
 (:goal  (and 
    (clear b4)
    (on b4 b3)
    (on b3 b1)
    (on b1 b2)
    (on-table b2))))
