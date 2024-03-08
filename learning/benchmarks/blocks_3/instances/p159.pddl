;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=159, seed=9

(define (problem blocksworld-159)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b3)
    (on-table b3)
    (clear b4)
    (on b4 b1)
    (on-table b1))
 (:goal  (and 
    (clear b4)
    (on b4 b2)
    (on-table b2)
    (clear b3)
    (on b3 b1)
    (on-table b1))))
