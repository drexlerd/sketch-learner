;; blocks=2, percentage_new_tower=40, out_folder=., instance_id=79, seed=9

(define (problem blocksworld-79)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (clear b2)
    (on-table b2)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on-table b2))))
