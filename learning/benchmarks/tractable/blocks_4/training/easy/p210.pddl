;; blocks=2, percentage_new_tower=40, out_folder=., instance_id=210, seed=0

(define (problem blocksworld-210)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on-table b2))))
