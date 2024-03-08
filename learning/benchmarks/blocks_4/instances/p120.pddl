;; blocks=4, percentage_new_tower=0, out_folder=., instance_id=120, seed=0

(define (problem blocksworld-120)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b1)
    (on b1 b2)
    (on b2 b4)
    (on-table b4))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on b1 b2)
    (on b2 b3)
    (on-table b3))))
