#!/bin/bash

sbatch -A snic2022-5-341 blocks_4_clear_1.sh
sbatch -A snic2022-5-341 blocks_4_clear_2.sh

sbatch -A snic2022-5-341 blocks_4_on_1.sh
sbatch -A snic2022-5-341 blocks_4_on_2.sh

sbatch -A snic2022-5-341 childsnack_1.sh

sbatch -A snic2022-5-341 delivery_1.sh
sbatch -A snic2022-5-341 delivery_2.sh

sbatch -A snic2022-5-341 gripper_1.sh
sbatch -A snic2022-5-341 gripper_2.sh

sbatch -A snic2022-5-341 miconic_1.sh
sbatch -A snic2022-5-341 miconic_2.sh

sbatch -A snic2022-5-341 reward_1.sh
sbatch -A snic2022-5-341 reward_2.sh

sbatch -A snic2022-5-341 spanner_1.sh
sbatch -A snic2022-5-341 spanner_2.sh

sbatch -A snic2022-5-341 visitall_1.sh
sbatch -A snic2022-5-341 visitall_2.sh
