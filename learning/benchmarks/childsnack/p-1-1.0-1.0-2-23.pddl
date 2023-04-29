; child-snack task with 1 children and 1.0 gluten factor 
; constant factor of 1.0
; random seed: 23

(define (problem prob-snack)
  (:domain child-snack)
  (:objects
    child1 - child
    bread1 - bread-portion
    content1 - content-portion
    tray1 tray2 - tray
    table1 table2 table3 - place
    sandw1 - sandwich
  )
  (:init
     (at tray1 kitchen)
     (at tray2 kitchen)
     (at_kitchen_bread bread1)
     (at_kitchen_content content1)
     (no_gluten_bread bread1)
     (no_gluten_content content1)
     (allergic_gluten child1)
     (waiting child1 table3)
     (notexist sandw1)
  )
  (:goal
    (and
     (served child1)
    )
  )
)
