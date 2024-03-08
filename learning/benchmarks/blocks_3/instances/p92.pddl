;; blocks=3, percentage_new_tower=10, out_folder=., instance_id=92, seed=2

(define (problem blocksworld-92)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (clear b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b3)
    (on b3 b1)
    (on b1 b2)
    (on-table b2))))
