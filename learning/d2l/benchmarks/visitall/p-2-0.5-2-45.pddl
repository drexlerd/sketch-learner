3
0
0
1
(define (problem grid-2)
(:domain grid-visit-all)
(:objects 
	loc-x1-y0
	loc-x1-y1
- place 
        
)
(:init
	(at-robot loc-x1-y1)
	(visited loc-x1-y1)
	(connected loc-x1-y0 loc-x1-y1)
 	(connected loc-x1-y1 loc-x1-y0)
 
)
(:goal
(and 
	(visited loc-x1-y1)
)
)
)
