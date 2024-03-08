(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	image0 - mode
	GroundStation0 - direction
	Planet1 - direction
	Planet2 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 GroundStation0)
	(supports instrument1 image0)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet2)
	(supports instrument2 image0)
	(calibration_target instrument2 GroundStation0)
	(supports instrument3 image0)
	(calibration_target instrument3 GroundStation0)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Planet2)
)
(:goal (and
	(have_image Planet1 image0)
	(have_image Planet2 image0)
))

)
