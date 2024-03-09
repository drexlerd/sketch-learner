;; blocks=5, percentage_new_tower=0, out_folder=., instance_id=505, seed=25

(define (problem blocksworld-505)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b3)
    (on b3 b2)
    (on b2 b1)
    (on b1 b5)
    (on-table b5))
 (:goal  (and 
    (clear b2)
    (on b2 b5)
    (on b5 b1)
    (on b1 b4)
    (on b4 b3)
    (on-table b3))))
