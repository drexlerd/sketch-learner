; child-snack task with 2 children and 0.0 gluten factor 
; constant factor of 1.0
; random seed: 9

(define (problem prob-snack)
  (:domain child-snack)
  (:objects
    child1 child2 - child
    bread1 bread2 - bread-portion
    content1 content2 - content-portion
    tray1 - tray
    table1 table2 table3 - place
    sandw1 sandw2 - sandwich
  )
  (:init
     (at tray1 kitchen)
     (at_kitchen_bread bread1)
     (at_kitchen_bread bread2)
     (at_kitchen_content content1)
     (at_kitchen_content content2)
     (not_allergic_gluten child2)
     (not_allergic_gluten child1)
     (waiting child1 table2)
     (waiting child2 table3)
     (notexist sandw1)
     (notexist sandw2)
  )
  (:goal
    (and
     (served child1)
     (served child2)
    )
  )
)
