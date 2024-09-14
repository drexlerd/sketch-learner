;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=568, seed=28

(define (problem blocksworld-568)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b4)
    (on b4 b1)
    (on b1 b5)
    (on b5 b3)
    (on-table b3))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on-table b1)
    (clear b5)
    (on b5 b2)
    (on b2 b3)
    (on-table b3))))
