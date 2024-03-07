#!/bin/bash
#
#SBATCH -J barman_0
#SBATCH -t 1-00:00:00
#SBATCH -C thin --exclusive
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=dominik.drexler@liu.se

bash ./runner.sh barman 0
