;; blocks=3, percentage_new_tower=0, out_folder=., instance_id=85, seed=5

(define (problem blocksworld-85)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b1)
    (on b1 b2)
    (on b2 b3)
    (on-table b3))
 (:goal  (and 
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))))
