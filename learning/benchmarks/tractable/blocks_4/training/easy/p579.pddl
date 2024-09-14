;; blocks=5, percentage_new_tower=40, out_folder=., instance_id=579, seed=9

(define (problem blocksworld-579)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on b3 b2)
    (on b2 b5)
    (on-table b5)
    (clear b4)
    (on-table b4))
 (:goal  (and 
    (clear b4)
    (on b4 b5)
    (on-table b5)
    (clear b1)
    (on-table b1)
    (clear b2)
    (on b2 b3)
    (on-table b3))))
