(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	infrared1 - mode
	spectrograph0 - mode
	Star0 - direction
	Star1 - direction
	Star2 - direction
	Phenomenon3 - direction
)
(:init
	(supports instrument0 infrared1)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Phenomenon3)
	(supports instrument1 spectrograph0)
	(supports instrument1 infrared1)
	(calibration_target instrument1 Star1)
	(supports instrument2 infrared1)
	(calibration_target instrument2 Star1)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star1)
)
(:goal (and
	(have_image Star2 spectrograph0)
	(have_image Phenomenon3 spectrograph0)
))

)
