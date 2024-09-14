#!/bin/bash

DATASET=$1  # tractable or ipc2023
DOMAIN_NAME=$2
WIDTH=$3

DOMAIN="${SKETCH_LEARNER_DIR}/learning/benchmarks/${DATASET}/${DOMAIN_NAME}/domain.pddl"
PROBLEMS="${SKETCH_LEARNER_DIR}/learning/benchmarks/${DATASET}/${DOMAIN_NAME}/training/easy"

WORKSPACE="${PWD}/workspace/${DOMAIN_NAME}_${WIDTH}"
RUN_ERR="${WORKSPACE}/run.err"
RUN_LOG="${WORKSPACE}/run.log"

mkdir -p ${WORKSPACE}

python3 ${SKETCH_LEARNER_DIR}/learning/experiments/scripts/${DOMAIN_NAME}.py --domain_filepath ${DOMAIN} --problems_directory ${PROBLEMS} --workspace ${WORKSPACE} --width ${WIDTH} 2> ${RUN_ERR} 1> ${RUN_LOG}
