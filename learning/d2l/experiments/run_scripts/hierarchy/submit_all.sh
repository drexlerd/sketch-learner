#!/bin/bash

sbatch -A snic2022-22-820 blocks_4_clear_1.sh
sbatch -A snic2022-22-820 blocks_4_clear_2.sh

sbatch -A snic2022-22-820 blocks_4_on_1.sh
sbatch -A snic2022-22-820 blocks_4_on_2.sh

# sbatch -A snic2022-22-820 childsnack_1.sh

sbatch -A snic2022-22-820 delivery_1.sh
sbatch -A snic2022-22-820 delivery_2.sh

sbatch -A snic2022-22-820 gripper_1.sh
sbatch -A snic2022-22-820 gripper_2.sh

sbatch -A snic2022-22-820 miconic_1.sh
sbatch -A snic2022-22-820 miconic_2.sh

sbatch -A snic2022-22-820 reward_1.sh
sbatch -A snic2022-22-820 reward_2.sh

sbatch -A snic2022-22-820 spanner_1.sh
sbatch -A snic2022-22-820 spanner_2.sh

sbatch -A snic2022-22-820 visitall_1.sh
sbatch -A snic2022-22-820 visitall_2.sh
