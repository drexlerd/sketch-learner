;; blocks=4, percentage_new_tower=20, out_folder=., instance_id=445, seed=25

(define (problem blocksworld-445)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on b3 b2)
    (on-table b2)
    (clear b4)
    (on-table b4))
 (:goal  (and 
    (clear b4)
    (on b4 b2)
    (on b2 b1)
    (on-table b1)
    (clear b3)
    (on-table b3))))
