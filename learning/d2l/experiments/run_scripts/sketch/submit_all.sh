#!/bin/bash

sbatch -A snic2021-5-488 blocks_4_clear_0.sh
sbatch -A snic2021-5-488 blocks_4_clear_1.sh
sbatch -A snic2021-5-488 blocks_4_clear_2.sh

sbatch -A snic2021-5-488 blocks_4_on_0.sh
sbatch -A snic2021-5-488 blocks_4_on_1.sh
sbatch -A snic2021-5-488 blocks_4_on_2.sh

sbatch -A snic2021-5-488 childsnack_0.sh
sbatch -A snic2021-5-488 childsnack_1.sh
sbatch -A snic2021-5-488 childsnack_2.sh

sbatch -A snic2021-5-488 delivery_0.sh
sbatch -A snic2021-5-488 delivery_1.sh
sbatch -A snic2021-5-488 delivery_2.sh

sbatch -A snic2021-5-488 grid_0.sh
sbatch -A snic2021-5-488 grid_1.sh
sbatch -A snic2021-5-488 grid_2.sh

sbatch -A snic2021-5-488 gripper_0.sh
sbatch -A snic2021-5-488 gripper_1.sh
sbatch -A snic2021-5-488 gripper_2.sh

sbatch -A snic2021-5-488 miconic_0.sh
sbatch -A snic2021-5-488 miconic_1.sh
sbatch -A snic2021-5-488 miconic_2.sh

sbatch -A snic2021-5-488 reward_0.sh
sbatch -A snic2021-5-488 reward_1.sh
sbatch -A snic2021-5-488 reward_2.sh

sbatch -A snic2021-5-488 spanner_0.sh
sbatch -A snic2021-5-488 spanner_1.sh
sbatch -A snic2021-5-488 spanner_2.sh

sbatch -A snic2021-5-488 visitall_0.sh
sbatch -A snic2021-5-488 visitall_1.sh
sbatch -A snic2021-5-488 visitall_2.sh
