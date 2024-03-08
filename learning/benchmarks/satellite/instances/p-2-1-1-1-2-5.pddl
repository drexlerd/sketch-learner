(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	image0 - mode
	Star1 - direction
	Star0 - direction
	Planet2 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 Star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star0)
)
(:goal (and
	(pointing satellite0 Star0)
	(have_image Planet2 image0)
))

)
