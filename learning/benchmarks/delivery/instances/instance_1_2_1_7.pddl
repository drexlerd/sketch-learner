
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instance file automatically generated by the Tarski FSTRIPS writer
;;; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem delivery-1x2-1)
    (:domain delivery)

    (:objects
        c_0_0 c_0_1 - cell
        p1 - package
        t1 - truck
    )

    (:init
        (adjacent c_0_1 c_0_0)
        (adjacent c_0_0 c_0_1)
        (at t1 c_0_0)
        (at p1 c_0_1)
        (empty t1)
    )

    (:goal
        (at p1 c_0_1)
    )

    
    
    
)

