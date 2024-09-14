#!/bin/bash

PARTITION="naiss2024-5-421"

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J barman_0 job.sh tractable barman 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J barman_1 job.sh tractable barman 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J barman_2 job.sh tractable barman 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_3_0 job.sh tractable blocks_3 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_3_1 job.sh tractable blocks_3 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_3_2 job.sh tractable blocks_3 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_clear_0 job.sh tractable blocks_4_clear 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_clear_1 job.sh tractable blocks_4_clear 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_clear_2 job.sh tractable blocks_4_clear 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_on_0 job.sh tractable blocks_4_on 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_on_1 job.sh tractable blocks_4_on 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_on_2 job.sh tractable blocks_4_on 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J childsnack_0 job.sh tractable childsnack 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J childsnack_1 job.sh tractable childsnack 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J childsnack_2 job.sh tractable childsnack 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J delivery_0 job.sh tractable delivery 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J delivery_1 job.sh tractable delivery 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J delivery_2 job.sh tractable delivery 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J gripper_0 job.sh tractable gripper 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J gripper_1 job.sh tractable gripper 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J gripper_2 job.sh tractable gripper 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J logistics_0 job.sh tractable logistics 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J logistics_1 job.sh tractable logistics 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J logistics_2 job.sh tractable logistics 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J miconic_0 job.sh tractable miconic 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J miconic_1 job.sh tractable miconic 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J miconic_2 job.sh tractable miconic 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J reward_0 job.sh tractable reward 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J reward_1 job.sh tractable reward 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J reward_2 job.sh tractable reward 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J satellite_0 job.sh tractable satellite 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J satellite_1 job.sh tractable satellite 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J satellite_2 job.sh tractable satellite 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J schedule_0 job.sh tractable schedule 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J schedule_1 job.sh tractable schedule 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J schedule_2 job.sh tractable schedule 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J spanner_0 job.sh tractable spanner 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J spanner_1 job.sh tractable spanner 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J spanner_2 job.sh tractable spanner 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J visitall_0 job.sh tractable visitall 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J visitall_1 job.sh tractable visitall 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J visitall_2 job.sh tractable visitall 2
