(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	image0 - mode
	GroundStation1 - direction
	GroundStation0 - direction
	Phenomenon2 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 GroundStation1)
	(supports instrument1 image0)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation1)
)
(:goal (and
	(have_image Phenomenon2 image0)
))

)
