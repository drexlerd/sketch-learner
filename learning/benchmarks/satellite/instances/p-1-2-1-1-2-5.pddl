(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	image0 - mode
	infrared1 - mode
	GroundStation0 - direction
	Star1 - direction
	Star2 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 infrared1)
	(calibration_target instrument0 Star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
)
(:goal (and
	(pointing satellite0 GroundStation0)
	(have_image Star2 infrared1)
))

)
