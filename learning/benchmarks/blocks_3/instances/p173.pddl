;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=173, seed=3

(define (problem blocksworld-173)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b3)
    (on b3 b4)
    (on b4 b5)
    (on b5 b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b2)
    (on-table b2)
    (clear b3)
    (on b3 b4)
    (on b4 b5)
    (on-table b5)
    (clear b1)
    (on-table b1))))
