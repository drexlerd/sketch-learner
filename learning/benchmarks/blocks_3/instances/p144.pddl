;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=144, seed=4

(define (problem blocksworld-144)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b4)
    (on b4 b3)
    (on b3 b1)
    (on-table b1)
    (clear b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on b2 b4)
    (on b4 b3)
    (on-table b3)
    (clear b1)
    (on-table b1))))
