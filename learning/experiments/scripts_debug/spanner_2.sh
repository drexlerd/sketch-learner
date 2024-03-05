#!/bin/bash
#
#SBATCH -J spanner_2
#SBATCH -t 1-00:00:00
#SBATCH -C thin --exclusive
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=dominik.drexler@liu.se

bash ./runner.sh spanner 2
