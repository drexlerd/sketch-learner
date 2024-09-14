;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=460, seed=10

(define (problem blocksworld-460)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on-table b3)
    (clear b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b4)
    (on b4 b3)
    (on-table b3)
    (clear b1)
    (on-table b1))))
