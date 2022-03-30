#! /usr/bin/env python3
import fd.grounding
import sys
import os
from libsiwr import SIWR_Planner
# MRJ: Profiler imports
#from prof import profiler_start, profiler_stop

def main( domain_file, problem_file, sketch_file, plan_file ) :
	task = SIWR_Planner( )

	# fd.grounding.default(domain_file, problem_file, task)
	fd.grounding.initialize_sketch_strips_problem( domain_file, problem_file, sketch_file, task )

	#MRJ: Uncomment to check what actions are being loaded
	#for i in range( 0, task.num_actions() ) :
	#	task.print_action( i )

	# MRJ: Setting planner parameters is as easy as setting the values
	# of Python object attributes

	# MRJ: Maximum bound on width is set to 1
	task.iw_bound = 2

	# MRJ: log filename set
	task.log_filename = 'iw.log'

	# MRJ: plan file
	task.plan_filename = plan_file

	# DD: We call the setup method in SIW_Planner
	task.setup()

	# DD: find solution
	task.solve()


def debug() :
	#main( "/home/dominik/downward-benchmarks/barman-sat14-strips/domain.pddl",
	#     "/home/dominik/downward-benchmarks/barman-sat14-strips/p5-10-4-13.pddl",
	#	 "barman.sketch",
	#	 "." )

	#main( "/home/dominik/downward-benchmarks/grid/domain.pddl",
	#     "/home/dominik/downward-benchmarks/grid/prob05.pddl",
	#	 "grid.sketch",
	#	 "." )

	#main( "/home/dominik/downward-benchmarks/tpp/domain.pddl",
	#     "/home/dominik/downward-benchmarks/tpp/p30.pddl",
	#	 "tpp.sketch",
	#	 "." )

	#main( "/home/dominik/downward-benchmarks/childsnack-sat14-strips/domain.pddl",
	#     "/home/dominik/downward-benchmarks/childsnack-sat14-strips/child-snack_pfile19-2.pddl",
	#	 "childsnack.sketch",
	#	 "." )

	main( "/home/dominik/downward-benchmarks/schedule/domain.pddl",
	     "/home/dominik/downward-benchmarks/schedule/probschedule-51-2.pddl",
		 "schedule.sketch",
		 "." )

    # some errors in distances
	#main("/home/dominik/downward-benchmarks/driverlog/domain.pddl",
	#     "/home/dominik/downward-benchmarks/driverlog/p01.pddl",
	#	 "driverlog.sketch",
	#	 "." )

    #main("domain.pddl",
	#     "p-1-3-16-1-1836107035.pddl",
	#	 "driverlog.sketch",
	#	 "." )

	#main( "/home/dominik/downward-benchmarks/floortile-sat14-strips/domain.pddl",
	#     "/home/dominik/downward-benchmarks/floortile-sat14-strips/p04-6-5-3.pddl",
	#	 "floortile.sketch",
	#	 "." )

if __name__ == "__main__":
	main( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )
	#debug()
