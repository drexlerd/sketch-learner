;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=195, seed=5

(define (problem blocksworld-195)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b4)
    (on-table b4)
    (clear b2)
    (on b2 b5)
    (on-table b5)
    (clear b3)
    (on-table b3)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b5)
    (on-table b5)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on b3 b4)
    (on b4 b2)
    (on-table b2))))
