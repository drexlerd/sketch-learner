(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	spectrograph0 - mode
	GroundStation0 - direction
	Phenomenon1 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 GroundStation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 GroundStation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon1)
)
(:goal (and
	(pointing satellite0 Phenomenon1)
	(pointing satellite1 Phenomenon1)
	(have_image Phenomenon1 spectrograph0)
))

)
