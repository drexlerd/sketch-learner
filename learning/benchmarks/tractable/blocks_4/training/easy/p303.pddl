;; blocks=3, percentage_new_tower=20, out_folder=., instance_id=303, seed=3

(define (problem blocksworld-303)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on-table b3)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b3)
    (on b3 b2)
    (on-table b2))))
