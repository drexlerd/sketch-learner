(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	image0 - mode
	infrared1 - mode
	GroundStation0 - direction
	Star1 - direction
	Phenomenon2 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 infrared1)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
)
(:goal (and
	(pointing satellite0 Star1)
	(have_image Star1 image0)
	(have_image Phenomenon2 infrared1)
))

)
