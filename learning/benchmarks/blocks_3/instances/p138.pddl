;; blocks=4, percentage_new_tower=10, out_folder=., instance_id=138, seed=8

(define (problem blocksworld-138)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b4)
    (on b4 b2)
    (on b2 b1)
    (on b1 b3)
    (on-table b3))
 (:goal  (and 
    (clear b2)
    (on b2 b4)
    (on b4 b1)
    (on b1 b3)
    (on-table b3))))
