(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	image0 - mode
	thermograph1 - mode
	Star1 - direction
	GroundStation0 - direction
	Phenomenon2 - direction
	Planet3 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 image0)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Planet3)
)
(:goal (and
	(have_image Phenomenon2 thermograph1)
	(have_image Planet3 thermograph1)
))

)
