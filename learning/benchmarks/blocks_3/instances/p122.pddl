;; blocks=4, percentage_new_tower=0, out_folder=., instance_id=122, seed=2

(define (problem blocksworld-122)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b1)
    (on b1 b2)
    (on b2 b4)
    (on b4 b3)
    (on-table b3))
 (:goal  (and 
    (clear b2)
    (on b2 b4)
    (on b4 b3)
    (on b3 b1)
    (on-table b1))))
