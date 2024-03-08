(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	spectrograph1 - mode
	infrared0 - mode
	Star0 - direction
	Phenomenon1 - direction
	Planet2 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon1)
)
(:goal (and
	(pointing satellite0 Phenomenon1)
	(have_image Phenomenon1 spectrograph1)
	(have_image Planet2 infrared0)
))

)
