


(define (problem schedule-p1-s1-c1-w2-o1)
(:domain schedule)
(:objects 
    P0
 - part
    CIRCULAR
 - ashape
    BLUE
 - colour
    ONE
    TWO
 - width
    FRONT
 - anorient
)
(:init
(HAS-PAINT IMMERSION-PAINTER BLUE)
(HAS-PAINT SPRAY-PAINTER BLUE)
(CAN-ORIENT DRILL-PRESS FRONT)
(CAN-ORIENT PUNCH FRONT)
(HAS-BIT DRILL-PRESS ONE)
(HAS-BIT PUNCH ONE)
(HAS-BIT DRILL-PRESS TWO)
(HAS-BIT PUNCH TWO)
(SHAPE P0 CIRCULAR)
(SURFACE-CONDITION P0 ROUGH)
(PAINTED P0 BLUE)
(HAS-HOLE P0 TWO FRONT)
(TEMPERATURE P0 COLD)
)
(:goal
(and
(SHAPE P0 CYLINDRICAL)
(SURFACE-CONDITION P0 ROUGH)
(HAS-HOLE P0 ONE FRONT)
)
)
)


