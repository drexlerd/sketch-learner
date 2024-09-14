#!/bin/bash

./job.sh tractable blocks_3 0
./job.sh tractable blocks_3 1
./job.sh tractable blocks_3 2

./job.sh tractable blocks_4_clear 0
./job.sh tractable blocks_4_clear 1
./job.sh tractable blocks_4_clear 2

./job.sh tractable blocks_4_on 0
./job.sh tractable blocks_4_on 1
./job.sh tractable blocks_4_on 2

./job.sh tractable delivery 0
./job.sh tractable delivery 1
./job.sh tractable delivery 2

./job.sh tractable gripper 0
./job.sh tractable gripper 1
./job.sh tractable gripper 2

./job.sh tractable miconic 0
./job.sh tractable miconic 1
./job.sh tractable miconic 2

./job.sh tractable reward 0
./job.sh tractable reward 1
./job.sh tractable reward 2

./job.sh tractable spanner 0
./job.sh tractable spanner 1
./job.sh tractable spanner 2

./job.sh tractable visitall 0
./job.sh tractable visitall 1
./job.sh tractable visitall 2
