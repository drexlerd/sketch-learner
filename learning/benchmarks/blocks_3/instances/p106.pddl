;; blocks=3, percentage_new_tower=20, out_folder=., instance_id=106, seed=6

(define (problem blocksworld-106)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b3)
    (on b3 b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on-table b3)
    (clear b2)
    (on b2 b1)
    (on-table b1))))
