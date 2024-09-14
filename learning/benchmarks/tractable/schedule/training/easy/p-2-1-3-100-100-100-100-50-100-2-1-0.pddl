


(define (problem schedule-p3-s2-c2-w1-o1)
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
    YELLOW
 - colour
    ONE
 - width
    FRONT
 - anorient
)
(:init
(HAS-PAINT IMMERSION-PAINTER BLUE)
(HAS-PAINT SPRAY-PAINTER BLUE)
(HAS-PAINT IMMERSION-PAINTER YELLOW)
(HAS-PAINT SPRAY-PAINTER YELLOW)
(CAN-ORIENT DRILL-PRESS FRONT)
(CAN-ORIENT PUNCH FRONT)
(HAS-BIT DRILL-PRESS ONE)
(HAS-BIT PUNCH ONE)
(SHAPE P0 CIRCULAR)
(SURFACE-CONDITION P0 ROUGH)
(PAINTED P0 YELLOW)
(TEMPERATURE P0 COLD)
(SHAPE P1 CIRCULAR)
(SURFACE-CONDITION P1 ROUGH)
(PAINTED P1 YELLOW)
(HAS-HOLE P1 ONE FRONT)
(TEMPERATURE P1 COLD)
(SHAPE P2 OBLONG)
(SURFACE-CONDITION P2 ROUGH)
(PAINTED P2 BLUE)
(HAS-HOLE P2 ONE FRONT)
(TEMPERATURE P2 COLD)
)
(:goal
(and
(SHAPE P0 CYLINDRICAL)
(SURFACE-CONDITION P0 SMOOTH)
(PAINTED P0 YELLOW)
(HAS-HOLE P0 ONE FRONT)
(SHAPE P1 CYLINDRICAL)
(SURFACE-CONDITION P1 ROUGH)
(PAINTED P1 BLUE)
(HAS-HOLE P1 ONE FRONT)
(SHAPE P2 CYLINDRICAL)
(SURFACE-CONDITION P2 ROUGH)
(PAINTED P2 BLUE)
(HAS-HOLE P2 ONE FRONT)
)
)
)


