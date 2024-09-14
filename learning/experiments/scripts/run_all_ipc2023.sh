#!/bin/bash

PARTITION="naiss2024-5-421"

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_0 job.sh ipc2023 blocks_4 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_1 job.sh ipc2023 blocks_4 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J blocks_4_2 job.sh ipc2023 blocks_4 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J childsnack_0 job.sh ipc2023 childsnack 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J childsnack_1 job.sh ipc2023 childsnack 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J childsnack_2 job.sh ipc2023 childsnack 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J ferry_on_0 job.sh ipc2023 ferry 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J ferry_on_1 job.sh ipc2023 ferry 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J ferry_on_2 job.sh ipc2023 ferry 2

# Domain requires too complex features
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J floortile_0 job.sh ipc2023 floortile 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J floortile_1 job.sh ipc2023 floortile 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J floortile_2 job.sh ipc2023 floortile 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J miconic_0 job.sh ipc2023 miconic 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J miconic_1 job.sh ipc2023 miconic 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J miconic_2 job.sh ipc2023 miconic 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J rovers_0 job.sh ipc2023 rovers 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J rovers_1 job.sh ipc2023 rovers 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J rovers_2 job.sh ipc2023 rovers 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J satellite_0 job.sh ipc2023 satellite 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J satellite_1 job.sh ipc2023 satellite 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J satellite_2 job.sh ipc2023 satellite 2

# Domain is intractable
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J sokoban_0 job.sh tractable sokoban 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J sokoban_1 job.sh tractable sokoban 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J sokoban_2 job.sh tractable sokoban 2

sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J spanner_0 job.sh ipc2023 spanner 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J spanner_1 job.sh ipc2023 spanner 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J spanner_2 job.sh ipc2023 spanner 2

# Domain is intractable
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J transport_0 job.sh ipc2023 transport 0
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J transport_1 job.sh ipc2023 transport 1
sbatch -A ${PARTITION} -t 1-00:00:00 -C thin --exclusive -J transport_2 job.sh ipc2023 transport 2
