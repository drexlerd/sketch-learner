;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=533, seed=23

(define (problem blocksworld-533)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b5)
    (on-table b5)
    (clear b3)
    (on b3 b1)
    (on b1 b4)
    (on-table b4))
 (:goal  (and 
    (clear b2)
    (on b2 b3)
    (on b3 b5)
    (on b5 b4)
    (on b4 b1)
    (on-table b1))))
