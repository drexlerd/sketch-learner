;; blocks=5, percentage_new_tower=0, out_folder=., instance_id=163, seed=3

(define (problem blocksworld-163)
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
    (clear b5)
    (on b5 b3)
    (on b3 b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1))))
