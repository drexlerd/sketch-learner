;; blocks=4, percentage_new_tower=40, out_folder=., instance_id=451, seed=1

(define (problem blocksworld-451)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 - object)
 (:init 
    (arm-empty)
    (clear b4)
    (on-table b4)
    (clear b3)
    (on b3 b2)
    (on-table b2)
    (clear b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b4)
    (on-table b4)
    (clear b3)
    (on b3 b2)
    (on-table b2))))
