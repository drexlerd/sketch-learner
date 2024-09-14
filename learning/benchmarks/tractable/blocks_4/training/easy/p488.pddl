;; blocks=5, percentage_new_tower=0, out_folder=., instance_id=488, seed=8

(define (problem blocksworld-488)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b3)
    (on b3 b4)
    (on b4 b5)
    (on b5 b2)
    (on-table b2))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on b2 b5)
    (on b5 b4)
    (on b4 b3)
    (on-table b3))))
