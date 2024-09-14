


(define (problem schedule-p3-s1-c1-w2-o1)
(:domain schedule)
(:objects 
    P0
    P1
    P2
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
(SHAPE P1 CYLINDRICAL)
(SURFACE-CONDITION P1 POLISHED)
(PAINTED P1 BLUE)
(HAS-HOLE P1 ONE FRONT)
(TEMPERATURE P1 COLD)
(SHAPE P2 CIRCULAR)
(SURFACE-CONDITION P2 ROUGH)
(PAINTED P2 BLUE)
(HAS-HOLE P2 ONE FRONT)
(TEMPERATURE P2 COLD)
)
(:goal
(and
(SHAPE P0 CYLINDRICAL)
(SURFACE-CONDITION P0 POLISHED)
(HAS-HOLE P0 ONE FRONT)
(SHAPE P1 CYLINDRICAL)
(SURFACE-CONDITION P1 SMOOTH)
(PAINTED P1 BLUE)
(HAS-HOLE P1 TWO FRONT)
(SHAPE P2 CYLINDRICAL)
(SURFACE-CONDITION P2 ROUGH)
(PAINTED P2 BLUE)
(HAS-HOLE P2 TWO FRONT)
)
)
)


