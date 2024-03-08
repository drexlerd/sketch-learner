;; blocks=5, percentage_new_tower=10, out_folder=., instance_id=171, seed=1

(define (problem blocksworld-171)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (clear b5)
    (on b5 b3)
    (on-table b3)
    (clear b2)
    (on b2 b4)
    (on-table b4)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b4)
    (on b4 b1)
    (on b1 b5)
    (on b5 b2)
    (on b2 b3)
    (on-table b3))))
