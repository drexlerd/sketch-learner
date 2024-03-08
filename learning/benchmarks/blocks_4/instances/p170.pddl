;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=170, seed=0

(define (problem blocksworld-170)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b5)
    (on b5 b1)
    (on b1 b2)
    (on b2 b3)
    (on b3 b4)
    (on-table b4))
 (:goal  (and 
    (clear b2)
    (on b2 b1)
    (on b1 b5)
    (on b5 b3)
    (on b3 b4)
    (on-table b4))))
