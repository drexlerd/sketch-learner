;; blocks=30, percentage_new_tower=10, out_folder=., instance_id=11, seed=0

(define (problem blocksworld-11)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b25 b26 b27 b28 b29 b30 - object)
 (:init 
    (clear b8)
    (on b8 b14)
    (on b14 b25)
    (on b25 b2)
    (on b2 b7)
    (on b7 b26)
    (on b26 b27)
    (on b27 b17)
    (on b17 b18)
    (on-table b18)
    (clear b11)
    (on b11 b30)
    (on b30 b23)
    (on b23 b29)
    (on b29 b24)
    (on b24 b13)
    (on b13 b1)
    (on b1 b16)
    (on-table b16)
    (clear b22)
    (on b22 b6)
    (on b6 b19)
    (on b19 b12)
    (on b12 b4)
    (on b4 b20)
    (on b20 b9)
    (on b9 b5)
    (on b5 b15)
    (on b15 b10)
    (on-table b10)
    (clear b28)
    (on b28 b3)
    (on b3 b21)
    (on-table b21))
 (:goal  (and 
    (clear b27)
    (on b27 b30)
    (on-table b30)
    (clear b8)
    (on b8 b24)
    (on b24 b1)
    (on b1 b18)
    (on b18 b12)
    (on b12 b25)
    (on b25 b6)
    (on b6 b17)
    (on b17 b28)
    (on b28 b29)
    (on b29 b9)
    (on-table b9)
    (clear b22)
    (on b22 b11)
    (on b11 b7)
    (on b7 b19)
    (on b19 b21)
    (on b21 b3)
    (on b3 b5)
    (on b5 b14)
    (on b14 b20)
    (on b20 b2)
    (on b2 b23)
    (on b23 b26)
    (on b26 b16)
    (on b16 b4)
    (on b4 b15)
    (on b15 b10)
    (on b10 b13)
    (on-table b13))))
