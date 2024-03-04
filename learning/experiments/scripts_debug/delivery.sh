#!/bin/bash
#
DOMAIN_NAME=$1
EXPERIMENT_NAME=$2
WIDTH=$3

CONCEPT_COMPLEXITY=9
ROLE_COMPLEXITY=9
BOOLEAN_COMPLEXITY=9
COUNT_NUMERICAL_COMPLEXITY=9
DISTANCE_NUMERICAL_COMPLEXITY=15
WORKSPACE="${PWD}/workspace/${DOMAIN_NAME}_${WIDTH}_${CONCEPT_COMPLEXITY}_${ROLE_COMPLEXITY}_${BOOLEAN_COMPLEXITY}_${COUNT_NUMERICAL_COMPLEXITY}_${DISTANCE_NUMERICAL_COMPLEXITY}"
DOMAIN="${PWD}/../../benchmarks/${DOMAIN_NAME}/domain.pddl"
TASK_DIR="${PWD}/../../benchmarks/${DOMAIN_NAME}/instances"
RUN_ERR="${WORKSPACE}/run.err"
RUN_LOG="${WORKSPACE}/run.log"

# Run a single task in the foreground.
rm -rf ${WORKSPACE}
mkdir -p ${WORKSPACE}
./../../main.py --domain ${DOMAIN} --task_dir ${TASK_DIR} --workspace ${WORKSPACE} -w ${WIDTH} -cc ${CONCEPT_COMPLEXITY} -rc ${ROLE_COMPLEXITY} -bc ${BOOLEAN_COMPLEXITY} -ncc ${COUNT_NUMERICAL_COMPLEXITY} -ndc ${DISTANCE_NUMERICAL_COMPLEXITY} --exp_id ${DOMAIN_NAME}:${EXPERIMENT_NAME} 2> ${RUN_ERR} 1> ${RUN_LOG}
exit_code=$?

if [ $exit_code -eq 0 ]; then
    # Remove run.err upon successful termination
    rm -f ${RUN_ERR}
fi
