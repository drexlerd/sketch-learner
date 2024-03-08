;; blocks=2, percentage_new_tower=0, out_folder=., instance_id=46, seed=6

(define (problem blocksworld-46)
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
