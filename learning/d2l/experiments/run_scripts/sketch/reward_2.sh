#!/bin/bash
#
#SBATCH -J reward_2_6_8
#SBATCH -t 7-00:00:00
#SBATCH -C fat --exclusive
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=dominik.drexler@liu.se

DOMAIN=reward
EXPERIMENT=sketch
WIDTH=2
MAX_SKETCH_RULES=6
COMPLEXITY=8

EXPERIMENT_NAME=${DOMAIN}_${EXPERIMENT}_${WIDTH}_${MAX_SKETCH_RULES}_${COMPLEXITY}

# Run a single task in the foreground.
mkdir -p ${D2L_PATH}/workspace/${EXPERIMENT_NAME}
./../../run.py ${DOMAIN}:${EXPERIMENT} -w ${WIDTH} -r ${MAX_SKETCH_RULES} -c ${COMPLEXITY} > "${D2L_PATH}/workspace/${EXPERIMENT_NAME}/run.log"
