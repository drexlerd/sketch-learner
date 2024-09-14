


(define (problem schedule-p3-s2-c1-w3-o1)
(:domain schedule)
(:objects 
    P0
    P1
    P2
 - part
    CIRCULAR
    OBLONG
 - ashape
    BLUE
 - colour
    ONE
    TWO
    THREE
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
(HAS-BIT DRILL-PRESS THREE)
(HAS-BIT PUNCH THREE)
(SHAPE P0 CIRCULAR)
(SURFACE-CONDITION P0 ROUGH)
(HAS-HOLE P0 THREE FRONT)
(TEMPERATURE P0 COLD)
(SHAPE P1 CIRCULAR)
(SURFACE-CONDITION P1 POLISHED)
(PAINTED P1 BLUE)
(HAS-HOLE P1 TWO FRONT)
(TEMPERATURE P1 COLD)
(SHAPE P2 CIRCULAR)
(SURFACE-CONDITION P2 SMOOTH)
(PAINTED P2 BLUE)
(HAS-HOLE P2 TWO FRONT)
(TEMPERATURE P2 COLD)
)
(:goal
(and
(SHAPE P0 CYLINDRICAL)
(SURFACE-CONDITION P0 POLISHED)
(PAINTED P0 BLUE)
(HAS-HOLE P0 THREE FRONT)
(SHAPE P1 CYLINDRICAL)
(SURFACE-CONDITION P1 SMOOTH)
(PAINTED P1 BLUE)
(HAS-HOLE P1 THREE FRONT)
(SHAPE P2 CYLINDRICAL)
(SURFACE-CONDITION P2 ROUGH)
(PAINTED P2 BLUE)
(HAS-HOLE P2 ONE FRONT)
)
)
)


