(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	spectrograph0 - mode
	GroundStation0 - direction
	Star1 - direction
	Phenomenon2 - direction
	Star3 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 Star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 GroundStation0)
)
(:goal (and
	(pointing satellite0 Star3)
	(have_image Phenomenon2 spectrograph0)
	(have_image Star3 spectrograph0)
))

)
