WIDTH=$1

DOMAIN_NAME=gripper
WORKSPACE="${PWD}/workspace/${DOMAIN_NAME}_${WIDTH}"
DOMAIN="${PWD}/../../benchmarks/${DOMAIN_NAME}/domain.pddl"
PROBLEMS="${PWD}/../../benchmarks/${DOMAIN_NAME}/instances_debug"
RUN_ERR="${WORKSPACE}/run.err"
RUN_LOG="${WORKSPACE}/run.log"

mkdir -p ${WORKSPACE}
python3 ./gripper.py --domain_filepath ${DOMAIN} --problems_directory ${PROBLEMS} --workspace ${WORKSPACE} --width ${WIDTH} 2> ${RUN_ERR} 1> ${RUN_LOG}
exit_code=$?

if [ $exit_code -eq 0 ]; then
    # Remove run.err upon successful termination
    rm -f ${RUN_ERR}
fi
