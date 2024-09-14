;; blocks=1, percentage_new_tower=0, out_folder=., instance_id=22, seed=22

(define (problem blocksworld-22)
 (:domain blocksworld)
 (:objects b1 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on-table b1))))
