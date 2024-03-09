;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=532, seed=22

(define (problem blocksworld-532)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b2)
    (on b2 b4)
    (on b4 b3)
    (on b3 b5)
    (on-table b5))
 (:goal  (and 
    (clear b5)
    (on b5 b1)
    (on b1 b3)
    (on b3 b2)
    (on-table b2)
    (clear b4)
    (on-table b4))))
