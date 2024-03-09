;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=567, seed=27

(define (problem blocksworld-567)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b1)
    (on b1 b3)
    (on b3 b2)
    (on b2 b5)
    (on-table b5))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on b2 b3)
    (on b3 b5)
    (on-table b5)
    (clear b4)
    (on-table b4))))
