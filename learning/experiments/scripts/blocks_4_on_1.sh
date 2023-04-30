#!/bin/bash
#
#SBATCH -J blocks_4_on_1
#SBATCH -t 4-00:00:00
#SBATCH -C thin --exclusive
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=dominik.drexler@liu.se

bash ./blocks_4_on.sh 1
