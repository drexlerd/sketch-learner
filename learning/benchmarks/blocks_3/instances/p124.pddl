;; blocks=4, percentage_new_tower=0, out_folder=., instance_id=124, seed=4

(define (problem blocksworld-124)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b3)
    (on b3 b1)
    (on b1 b4)
    (on b4 b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on b2 b4)
    (on b4 b3)
    (on b3 b1)
    (on-table b1))))
