#!/bin/bash
#
# e.g. dfsplan=${PARTITION}
PARTITION=$1

# Solved domains
sbatch -A ${PARTITION} blocks_4_clear_0.sh
#sbatch -A ${PARTITION} blocks_4_clear_1.sh
#sbatch -A ${PARTITION} blocks_4_clear_2.sh

sbatch -A ${PARTITION} blocks_4_on_0.sh
#sbatch -A ${PARTITION} blocks_4_on_1.sh
#sbatch -A ${PARTITION} blocks_4_on_2.sh

sbatch -A ${PARTITION} delivery_0.sh
#sbatch -A ${PARTITION} delivery_1.sh
#sbatch -A ${PARTITION} delivery_2.sh

sbatch -A ${PARTITION} ferry_0.sh
#sbatch -A ${PARTITION} ferry_1.sh
#sbatch -A ${PARTITION} ferry_2.sh

sbatch -A ${PARTITION} gripper_0.sh
#sbatch -A ${PARTITION} gripper_1.sh
#sbatch -A ${PARTITION} gripper_2.sh

sbatch -A ${PARTITION} miconic_0.sh
#sbatch -A ${PARTITION} miconic_1.sh
#sbatch -A ${PARTITION} miconic_2.sh

sbatch -A ${PARTITION} reward_0.sh
#sbatch -A ${PARTITION} reward_1.sh
#sbatch -A ${PARTITION} reward_2.sh

sbatch -A ${PARTITION} spanner_0.sh
#sbatch -A ${PARTITION} spanner_1.sh
#sbatch -A ${PARTITION} spanner_2.sh

sbatch -A ${PARTITION} visitall_0.sh
#sbatch -A ${PARTITION} visitall_1.sh
#sbatch -A ${PARTITION} visitall_2.sh


# Challenging domains
#sbatch -A ${PARTITION} barman_0.sh
#sbatch -A ${PARTITION} barman_1.sh
#sbatch -A ${PARTITION} barman_2.sh

sbatch -A ${PARTITION} blocks_3_0.sh
#sbatch -A ${PARTITION} blocks_3_1.sh
#sbatch -A ${PARTITION} blocks_3_2.sh

#sbatch -A ${PARTITION} blocks_4_0.sh
#sbatch -A ${PARTITION} blocks_4_1.sh
#sbatch -A ${PARTITION} blocks_4_2.sh

#sbatch -A ${PARTITION} childsnack_0.sh
#sbatch -A ${PARTITION} childsnack_1.sh
#sbatch -A ${PARTITION} childsnack_2.sh

#sbatch -A ${PARTITION} driverlog_0.sh
#sbatch -A ${PARTITION} driverlog_1.sh
#sbatch -A ${PARTITION} driverlog_2.sh

#sbatch -A ${PARTITION} grid_0.sh
#sbatch -A ${PARTITION} grid_1.sh
#sbatch -A ${PARTITION} grid_2.sh

#sbatch -A ${PARTITION} hiking_0.sh
#sbatch -A ${PARTITION} hiking_1.sh
#sbatch -A ${PARTITION} hiking_2.sh

#sbatch -A ${PARTITION} logistics_0.sh
#sbatch -A ${PARTITION} logistics_1.sh
#sbatch -A ${PARTITION} logistics_2.sh

#sbatch -A ${PARTITION} rovers_0.sh
#sbatch -A ${PARTITION} rovers_1.sh
#sbatch -A ${PARTITION} rovers_2.sh

#sbatch -A ${PARTITION} satellite_0.sh
#sbatch -A ${PARTITION} satellite_1.sh
#sbatch -A ${PARTITION} satellite_2.sh
