; Domain designed by Alfonso Gerevini and Alessandro Saetti
; This file has been automatically generated by the generator available from
; http://zeus.ing.unibs.it/ipc-5/generators/index.html

(define (problem TPP)
(:domain TPP-Propositional)
(:objects
	goods1 - goods
	truck1 - truck
	market1 market2 - market
	depot1 depot2 - depot
	level0 level1 level2 - level)

(:init
	(next level1 level0)
	(next level2 level1)
	(ready-to-load goods1 market1 level0)
	(ready-to-load goods1 market2 level0)
	(stored goods1 level0)
	(loaded goods1 truck1 level0)
	(connected market1 market2)
	(connected market2 market1)
	(connected depot1 market2)
	(connected market2 depot1)
	(connected depot2 market2)
	(connected market2 depot2)
	(on-sale goods1 market1 level2)
	(on-sale goods1 market2 level0)
	(at truck1 depot2))

(:goal (and
	(stored goods1 level2)))

)
