;; blocks=3, percentage_new_tower=40, out_folder=., instance_id=352, seed=22

(define (problem blocksworld-352)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b3)
    (on-table b3)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b1)
    (on b1 b2)
    (on-table b2))))
