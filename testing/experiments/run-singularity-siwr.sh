#!/bin/bash

set -euo pipefail

if [[ $# != 6 ]]; then
    echo "usage: $(basename "$0") image domain_file problem_file sketch_file width plan_file" 1>&2
    exit 2
fi

if [ -f $PWD/$6 ]; then
    echo "Error: remove $PWD/$6" 1>&2
    exit 2
fi

set +e
# Some planners print to stderr when running out of memory, so we redirect stderr to stdout.
{ /usr/bin/time -o /dev/stdout -f "Singularity runtime: %es real, %Us user, %Ss sys" \
  singularity run -C -H $PWD $1 $PWD/$2 $PWD/$3 $PWD/$4 $5 $6 ; } 2>&1
set -e

printf "\nRun VAL\n\n"

if [ -f $PWD/$6 ]; then
    echo "Found plan file."
    validate $PWD/$2 $PWD/$3 $PWD/$6
else
    echo "No plan file."
    validate $PWD/$2 $PWD/$3
fi
