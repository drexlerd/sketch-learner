(define (problem DLOG-2-2-2)
	(:domain driverlog)
	(:objects
	driver1
	truck1
	package1
	s0
	s1
	s2
	p1-0
	p1-2
	)
	(:init
	(at driver1 s2)
	(DRIVER driver1)
	(at truck1 s0)
	(empty truck1)
	(TRUCK truck1)
	(at package1 s0)
	(OBJ package1)
	(LOCATION s0)
	(LOCATION s1)
	(LOCATION s2)
	(LOCATION p1-0)
	(LOCATION p1-2)
	(path s1 p1-0)
	(path p1-0 s1)
	(path s0 p1-0)
	(path p1-0 s0)
	(path s1 p1-2)
	(path p1-2 s1)
	(path s2 p1-2)
	(path p1-2 s2)
	(link s0 s1)
	(link s1 s0)
	(link s0 s2)
	(link s2 s0)
	(link s2 s1)
	(link s1 s2)
)
	(:goal (and
	(at driver1 s1)
	))


)
