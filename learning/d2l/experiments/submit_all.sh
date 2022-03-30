#!/bin/bash

sbatch -A snic2021-5-330 blocks_4_clear_0.sh
sbatch -A snic2021-5-330 blocks_4_clear_1.sh
sbatch -A snic2021-5-330 blocks_4_clear_2.sh

sbatch -A snic2021-5-330 blocks_4_on_0.sh
sbatch -A snic2021-5-330 blocks_4_on_1.sh
sbatch -A snic2021-5-330 blocks_4_on_2.sh

sbatch -A snic2021-5-330 childsnack_0.sh
sbatch -A snic2021-5-330 childsnack_1.sh
sbatch -A snic2021-5-330 childsnack_2.sh

sbatch -A snic2021-5-330 delivery_0.sh
sbatch -A snic2021-5-330 delivery_1.sh
sbatch -A snic2021-5-330 delivery_2.sh

sbatch -A snic2021-5-330 grid_0.sh
sbatch -A snic2021-5-330 grid_1.sh
sbatch -A snic2021-5-330 grid_2.sh

sbatch -A snic2021-5-330 gripper_0.sh
sbatch -A snic2021-5-330 gripper_1.sh
sbatch -A snic2021-5-330 gripper_2.sh

sbatch -A snic2021-5-330 miconic_0.sh
sbatch -A snic2021-5-330 miconic_1.sh
sbatch -A snic2021-5-330 miconic_2.sh

sbatch -A snic2021-5-330 reward_0.sh
sbatch -A snic2021-5-330 reward_1.sh
sbatch -A snic2021-5-330 reward_2.sh

sbatch -A snic2021-5-330 spanner_0.sh
sbatch -A snic2021-5-330 spanner_1.sh
sbatch -A snic2021-5-330 spanner_2.sh

sbatch -A snic2021-5-330 visitall_0.sh
sbatch -A snic2021-5-330 visitall_1.sh
sbatch -A snic2021-5-330 visitall_2.sh
