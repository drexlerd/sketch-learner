;; blocks=2, percentage_new_tower=0, out_folder=., instance_id=42, seed=2

(define (problem blocksworld-42)
 (:domain blocksworld)
 (:objects b1 b2 - object)
 (:init 
    (clear b2)
    (on b2 b1)
    (on-table b1))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on-table b2))))
