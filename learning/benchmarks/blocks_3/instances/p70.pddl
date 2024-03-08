;; blocks=2, percentage_new_tower=40, out_folder=., instance_id=70, seed=0

(define (problem blocksworld-70)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (clear b1)
    (on b1 b2)
    (on-table b2))
 (:goal  (and 
    (clear b1)
    (on-table b1)
    (clear b2)
    (on-table b2))))
