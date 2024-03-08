;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=177, seed=7

(define (problem blocksworld-177)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b4)
    (on b4 b2)
    (on b2 b1)
    (on b1 b3)
    (on b3 b5)
    (on-table b5))
 (:goal  (and 
    (clear b3)
    (on b3 b2)
    (on b2 b4)
    (on b4 b1)
    (on b1 b5)
    (on-table b5))))
