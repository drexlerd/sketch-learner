#!/bin/bash
#
#SBATCH -J blocks3_2_9_9
#SBATCH -t 3-00:00:00
#SBATCH -C fat --exclusive
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=dominik.drexler@liu.se

DOMAIN=blocks_3
EXPERIMENT=sketch
WIDTH=2
CONCEPT_COMPLEXITY=9
ROLE_COMPLEXITY=9
BOOLEAN_COMPLEXITY=9
COUNT_NUMERICAL_COMPLEXITY=9
DISTANCE_NUMERICAL_COMPLEXITY=9

EXPERIMENT_NAME=${DOMAIN}_${EXPERIMENT}_${WIDTH}_${CONCEPT_COMPLEXITY}_${ROLE_COMPLEXITY}_${BOOLEAN_COMPLEXITY}_${COUNT_NUMERICAL_COMPLEXITY}_${DISTANCE_NUMERICAL_COMPLEXITY}

# Run a single task in the foreground.
mkdir -p ${D2L_PATH}/workspace/${EXPERIMENT_NAME}
./../../run.py ${DOMAIN}:${EXPERIMENT} -w ${WIDTH} -cc ${CONCEPT_COMPLEXITY} -rc ${ROLE_COMPLEXITY} -bc ${BOOLEAN_COMPLEXITY} -ncc ${COUNT_NUMERICAL_COMPLEXITY} -ndc ${DISTANCE_NUMERICAL_COMPLEXITY} > "${D2L_PATH}/workspace/${EXPERIMENT_NAME}/run.log"
