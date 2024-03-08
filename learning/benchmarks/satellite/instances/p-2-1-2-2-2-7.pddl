(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	image0 - mode
	GroundStation0 - direction
	Star1 - direction
	Star2 - direction
	Star3 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 Star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 Star2)
	(supports instrument1 image0)
	(calibration_target instrument1 Star1)
	(supports instrument2 image0)
	(calibration_target instrument2 Star1)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Star2)
)
(:goal (and
	(have_image Star2 image0)
	(have_image Star3 image0)
))

)
