#!/bin/bash

sbatch -A snic2021-5-330 gripper_0.sh
sbatch -A snic2021-5-330 gripper_1.sh
sbatch -A snic2021-5-330 gripper_2.sh

sbatch -A snic2021-5-330 spanner_0.sh
sbatch -A snic2021-5-330 spanner_1.sh
sbatch -A snic2021-5-330 spanner_2.sh

sbatch -A snic2021-5-330 visitall_0.sh
sbatch -A snic2021-5-330 visitall_1.sh
sbatch -A snic2021-5-330 visitall_2.sh
