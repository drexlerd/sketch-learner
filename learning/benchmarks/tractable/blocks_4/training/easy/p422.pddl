;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=422, seed=2

(define (problem blocksworld-422)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b4)
    (on b4 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b3)
    (on b3 b4)
    (on b4 b1)
    (on-table b1))))
