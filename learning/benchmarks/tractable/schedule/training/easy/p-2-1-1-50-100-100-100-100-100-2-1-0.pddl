


(define (problem schedule-p1-s2-c2-w1-o1)
(:domain schedule)
(:objects 
    P0
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
(HAS-HOLE P0 ONE FRONT)
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


