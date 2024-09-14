


(define (problem schedule-p2-s1-c3-w3-o1)
(:domain schedule)
(:objects 
    P0
    P1
 - part
    CIRCULAR
 - ashape
    BLUE
    YELLOW
    RED
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
(HAS-PAINT IMMERSION-PAINTER YELLOW)
(HAS-PAINT SPRAY-PAINTER YELLOW)
(HAS-PAINT IMMERSION-PAINTER RED)
(HAS-PAINT SPRAY-PAINTER RED)
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
(SHAPE P1 CYLINDRICAL)
(SURFACE-CONDITION P1 POLISHED)
(PAINTED P1 YELLOW)
(TEMPERATURE P1 COLD)
)
(:goal
(and
(SHAPE P0 CYLINDRICAL)
(SURFACE-CONDITION P0 ROUGH)
(HAS-HOLE P0 ONE FRONT)
(SHAPE P1 CYLINDRICAL)
(SURFACE-CONDITION P1 SMOOTH)
(HAS-HOLE P1 ONE FRONT)
)
)
)


