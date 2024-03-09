;; blocks=3, percentage_new_tower=20, out_folder=., instance_id=321, seed=21

(define (problem blocksworld-321)
 (:domain blocksworld)
 (:objects b1 b2 b3 - object)
 (:init 
    (arm-empty)
    (clear b2)
    (on-table b2)
    (clear b1)
    (on-table b1)
    (clear b3)
    (on-table b3))
 (:goal  (and 
    (clear b1)
    (on b1 b2)
    (on-table b2)
    (clear b3)
    (on-table b3))))
