;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=476, seed=26

(define (problem blocksworld-476)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on-table b4)
    (clear b3)
    (on b3 b1)
    (on-table b1)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on-table b1)
    (clear b3)
    (on b3 b2)
    (on-table b2))))
