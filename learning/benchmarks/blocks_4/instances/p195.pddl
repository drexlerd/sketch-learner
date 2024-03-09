;; blocks=2, percentage_new_tower=20, out_folder=., instance_id=195, seed=15

(define (problem blocksworld-195)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on-table b2))))
