(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	spectrograph1 - mode
	thermograph0 - mode
	Star0 - direction
	Phenomenon1 - direction
	Phenomenon2 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon1)
)
(:goal (and
	(pointing satellite0 Phenomenon1)
	(have_image Phenomenon1 thermograph0)
	(have_image Phenomenon2 thermograph0)
))

)
