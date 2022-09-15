#!/bin/bash
#
#SBATCH -J miconic_1_8
#SBATCH -t 3-00:00:00
#SBATCH -C fat --exclusive
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=dominik.drexler@liu.se

DOMAIN=miconic
EXPERIMENT=sketch
WIDTH=1
COMPLEXITY=8

EXPERIMENT_NAME=${DOMAIN}_${EXPERIMENT}_${WIDTH}_${COMPLEXITY}

# Run a single task in the foreground.
mkdir -p ${D2L_PATH}/workspace/${EXPERIMENT_NAME}
./../../run.py ${DOMAIN}:${EXPERIMENT} -w ${WIDTH} -c ${COMPLEXITY} > "${D2L_PATH}/workspace/${EXPERIMENT_NAME}/run.log"
