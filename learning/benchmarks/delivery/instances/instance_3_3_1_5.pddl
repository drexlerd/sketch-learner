
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instance file automatically generated by the Tarski FSTRIPS writer
;;; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem delivery-3x3-1)
    (:domain delivery)

    (:objects
        c_0_0 c_0_1 c_0_2 c_1_0 c_1_1 c_1_2 c_2_0 c_2_1 c_2_2 - cell
        p1 - package
        t1 - truck
    )

    (:init
        (adjacent c_1_0 c_1_1)
        (adjacent c_1_1 c_1_2)
        (adjacent c_0_0 c_1_0)
        (adjacent c_0_2 c_0_1)
        (adjacent c_1_0 c_0_0)
        (adjacent c_0_2 c_1_2)
        (adjacent c_1_1 c_2_1)
        (adjacent c_1_0 c_2_0)
        (adjacent c_2_0 c_2_1)
        (adjacent c_2_1 c_1_1)
        (adjacent c_1_1 c_1_0)
        (adjacent c_2_1 c_2_2)
        (adjacent c_1_2 c_1_1)
        (adjacent c_0_0 c_0_1)
        (adjacent c_1_2 c_2_2)
        (adjacent c_1_2 c_0_2)
        (adjacent c_2_0 c_1_0)
        (adjacent c_2_2 c_1_2)
        (adjacent c_2_1 c_2_0)
        (adjacent c_0_1 c_1_1)
        (adjacent c_2_2 c_2_1)
        (adjacent c_0_1 c_0_2)
        (adjacent c_1_1 c_0_1)
        (adjacent c_0_1 c_0_0)
        (at p1 c_0_2)
        (at t1 c_2_2)
        (empty t1)
    )

    (:goal
        (at p1 c_0_0)
    )

    
    
    
)

