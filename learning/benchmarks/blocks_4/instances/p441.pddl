;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=441, seed=21

(define (problem blocksworld-441)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b1)
    (on-table b1)
    (clear b2)
    (on b2 b4)
    (on-table b4))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on b2 b3)
    (on b3 b4)
    (on-table b4))))
