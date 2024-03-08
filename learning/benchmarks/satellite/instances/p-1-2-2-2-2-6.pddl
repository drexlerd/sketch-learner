(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	infrared0 - mode
	thermograph1 - mode
	GroundStation1 - direction
	GroundStation0 - direction
	Phenomenon2 - direction
	Planet3 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon2)
	(supports instrument1 infrared0)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon2)
)
(:goal (and
	(pointing satellite1 Phenomenon2)
	(have_image Phenomenon2 thermograph1)
	(have_image Planet3 infrared0)
))

)
