;; blocks=4, percentage_new_tower=0, out_folder=., instance_id=127, seed=7

(define (problem blocksworld-127)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (clear b4)
    (on b4 b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b2)
    (on b2 b1)
    (on b1 b4)
    (on b4 b3)
    (on-table b3))))
