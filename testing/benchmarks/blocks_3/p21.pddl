;; blocks=40, percentage_new_tower=10, out_folder=., instance_id=21, seed=0

(define (problem blocksworld-21)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b25 b26 b27 b28 b29 b30 b31 b32 b33 b34 b35 b36 b37 b38 b39 b40 - object)
 (:init 
    (clear b16)
    (on b16 b38)
    (on-table b38)
    (clear b32)
    (on b32 b2)
    (on b2 b9)
    (on b9 b12)
    (on b12 b4)
    (on b4 b25)
    (on b25 b15)
    (on b15 b40)
    (on b40 b6)
    (on-table b6)
    (clear b17)
    (on b17 b33)
    (on b33 b34)
    (on-table b34)
    (clear b22)
    (on b22 b37)
    (on b37 b28)
    (on b28 b18)
    (on b18 b19)
    (on b19 b21)
    (on b21 b36)
    (on b36 b27)
    (on b27 b30)
    (on b30 b39)
    (on b39 b7)
    (on b7 b29)
    (on b29 b10)
    (on b10 b23)
    (on b23 b1)
    (on b1 b14)
    (on b14 b24)
    (on-table b24)
    (clear b26)
    (on b26 b3)
    (on b3 b35)
    (on b35 b5)
    (on b5 b11)
    (on b11 b8)
    (on-table b8)
    (clear b20)
    (on b20 b31)
    (on b31 b13)
    (on-table b13))
 (:goal  (and 
    (clear b5)
    (on b5 b13)
    (on b13 b34)
    (on-table b34)
    (clear b28)
    (on b28 b6)
    (on b6 b36)
    (on b36 b3)
    (on b3 b4)
    (on b4 b31)
    (on b31 b32)
    (on b32 b14)
    (on b14 b11)
    (on b11 b8)
    (on b8 b16)
    (on b16 b29)
    (on b29 b24)
    (on b24 b22)
    (on b22 b2)
    (on b2 b35)
    (on b35 b18)
    (on b18 b19)
    (on b19 b10)
    (on b10 b15)
    (on b15 b21)
    (on b21 b37)
    (on b37 b40)
    (on b40 b30)
    (on b30 b20)
    (on b20 b38)
    (on b38 b39)
    (on b39 b17)
    (on b17 b26)
    (on b26 b7)
    (on b7 b27)
    (on b27 b1)
    (on b1 b33)
    (on b33 b23)
    (on-table b23)
    (clear b12)
    (on-table b12)
    (clear b25)
    (on b25 b9)
    (on-table b9))))
