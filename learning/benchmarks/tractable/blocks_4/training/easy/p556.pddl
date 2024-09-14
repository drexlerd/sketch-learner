;; blocks=5, percentage_new_tower=20, out_folder=., instance_id=556, seed=16

(define (problem blocksworld-556)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on b4 b3)
    (on b3 b1)
    (on-table b1)
    (clear b5)
    (on-table b5)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b5)
    (on-table b5)
    (clear b1)
    (on b1 b4)
    (on b4 b3)
    (on b3 b2)
    (on-table b2))))
